# src/scraping/telegram_scraper.py

import os
import asyncio
import json
from datetime import datetime
import logging
import re # For cleaning channel names
import random # For introducing random delays

from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.errors import SessionPasswordNeededError, FloodWaitError, PhoneNumberBannedError
from dotenv import load_dotenv

# --- Configuration and Setup ---

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("logs/telegram_scraper.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
# Ensure SESSION_NAME is unique and ideally tied to the user/account
# This ensures separate session files if you ever use multiple accounts
SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'telegram_session')

# Data lake paths (inside the Docker container)
DATA_LAKE_BASE_PATH = os.getenv('DATA_LAKE_PATH', '/app/data/raw')
RAW_MESSAGES_PATH = os.path.join(DATA_LAKE_BASE_PATH, 'telegram_messages')
RAW_IMAGES_PATH = os.path.join(DATA_LAKE_BASE_PATH, 'telegram_images')

# Ensure directories exist
# These should ideally be mounted volumes in Docker for persistence
os.makedirs("logs", exist_ok=True)
os.makedirs(RAW_MESSAGES_PATH, exist_ok=True)
os.makedirs(RAW_IMAGES_PATH, exist_ok=True)

# List of public Telegram channels to scrape
TELEGRAM_CHANNELS = [
    'https://t.me/chemed_chem',
    'https://t.me/lobelia4cosmetics',
    'https://t.me/tikvahpharma',
    # Add more channels from https://et.tgstat.com/medicine as needed
]

# --- Policy-Friendly Parameters ---
# These values are crucial for avoiding bans. Adjust based on observation.
MIN_CHANNEL_DELAY_SECONDS = 10  # Minimum delay between scraping different channels
MAX_CHANNEL_DELAY_SECONDS = 30  # Maximum delay between scraping different channels
MESSAGE_BATCH_SIZE = 100        # How many messages to fetch in one iteration
MIN_MESSAGE_DELAY_SECONDS = 0.5 # Minimum delay after processing a message batch
MAX_MESSAGE_DELAY_SECONDS = 2   # Maximum delay after processing a message batch
DOWNLOAD_MEDIA_DELAY_SECONDS = 0.5 # Delay after each media download

# --- Helper Functions ---

def clean_channel_name(channel_entity_title):
    """Cleans a channel title to be suitable for a directory name."""
    # Allow spaces but replace with underscore, remove other special chars
    cleaned_name = re.sub(r'[^\w\s-]', '', channel_entity_title).replace(' ', '_').lower()
    return cleaned_name if cleaned_name else "unknown_channel"

async def download_media(client, message, channel_dir):
    """Downloads media (photos, documents) from a message."""
    if not message.media:
        return None, None

    media_type = None
    if isinstance(message.media, MessageMediaPhoto):
        media_type = 'photo'
    elif isinstance(message.media, MessageMediaDocument) and message.media.document.mime_type and message.media.document.mime_type.startswith('image/'):
        media_type = 'document_image'
    else:
        return None, None # Not an image we want to download

    file_extension = ''
    if media_type == 'photo':
        file_extension = '.jpg' # Telethon often converts photos to JPG
    elif message.media.document and message.media.document.mime_type:
        ext_match = re.search(r'\/(jpeg|png|gif|webp)$', message.media.document.mime_type)
        if ext_match:
            file_extension = f".{ext_match.group(1)}"
        elif message.media.document.attributes:
            for attr in message.media.document.attributes:
                if hasattr(attr, 'file_name'):
                    _, ext = os.path.splitext(attr.file_name)
                    if ext:
                        file_extension = ext
                        break
    if not file_extension: # Ensure there's always an extension
        file_extension = '.bin' # Fallback for unknown image types

    try:
        # Ensure the image directory exists
        image_dir_path = os.path.join(RAW_IMAGES_PATH, channel_dir)
        os.makedirs(image_dir_path, exist_ok=True)

        # Construct unique file path
        # Use message ID and date for uniqueness. Avoid too long names.
        file_name = f"{message.id}_{message.date.strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(image_dir_path, file_name)

        # Download the media
        logger.info(f"Downloading media {message.id} to {file_path}")
        downloaded_path = await client.download_media(message, file=file_path)
        logger.info(f"Downloaded media to: {downloaded_path}")

        # Introduce a small delay after each media download
        await asyncio.sleep(DOWNLOAD_MEDIA_DELAY_SECONDS)

        return downloaded_path, media_type
    except FloodWaitError as e:
        logger.warning(f"FloodWaitError during media download for message {message.id}: Must wait {e.seconds} seconds. Waiting...")
        await asyncio.sleep(e.seconds + random.uniform(2, 5)) # Add buffer to wait
        return None, None # Don't retry this specific download, let next run handle it
    except Exception as e:
        logger.error(f"Error downloading media for message {message.id} in channel {channel_dir}: {e}", exc_info=True)
        return None, None

async def scrape_channel(client, channel_url):
    """Scrapes messages and media from a single Telegram channel."""
    try:
        entity = await client.get_entity(channel_url)
        channel_name = clean_channel_name(entity.title)
        logger.info(f"Scraping channel: {entity.title} (ID: {entity.id})")

        messages_data = []
        downloaded_images = []
        
        # Implement incremental scraping by storing the last scraped message ID
        # This prevents re-scraping old messages unnecessarily and reduces API calls
        # For simplicity, we'll use a placeholder. In a real scenario, you might
        # load this from a small database or a file.
        last_scraped_message_id = 0 # Placeholder for initial run.

        # Fetch messages in batches to avoid large single requests
        # and allow for delays between batches.
        # This will fetch messages newer than last_scraped_message_id
        # Set `limit` to MESSAGE_BATCH_SIZE
        # You might want to iterate until `offset_id` is 0 or no more messages are returned
        # For a full scrape, remove `offset_id` and iterate. For incremental, use `min_id`.
        
        # For a more robust incremental scrape, you would store `message.id`
        # and pass it as `min_id` in subsequent runs.
        # Example: messages = client.iter_messages(entity, min_id=last_scraped_message_id, limit=MESSAGE_BATCH_SIZE)

        # Iterating without a 'limit' (or with limit=None) fetches all.
        # For initial full scrape, this is fine. For subsequent, use min_id.
        messages_fetched_count = 0
        
        async for message in client.iter_messages(entity, min_id=last_scraped_message_id):
            message_info = {
                'message_id': message.id,
                'sender_id': message.sender_id,
                'sender_type': message.peer_id.__class__.__name__ if message.peer_id else None,
                'date': message.date.isoformat(),
                'message_text': message.message,
                'views': message.views,
                'forwards': message.forwards,
                'replies': message.replies.replies if message.replies else None,
                'media_present': bool(message.media),
                'media_type': None,
                'media_file_path': None,
                'post_author': message.post_author,
                'grouped_id': message.grouped_id,
                'is_channel_post': message.post,
                'channel_id': entity.id,
                'channel_title': entity.title,
                'channel_username': entity.username,
                'raw_message_json': message.to_dict() # Store the full raw message for schema flexibility
            }

            if message.media:
                media_path, media_type = await download_media(client, message, channel_name)
                message_info['media_file_path'] = media_path
                message_info['media_type'] = media_type
                if media_path:
                    downloaded_images.append({
                        'message_id': message.id,
                        'channel_id': entity.id,
                        'file_path': media_path,
                        'media_type': media_type
                    })
            
            messages_data.append(message_info)
            messages_fetched_count += 1

            # Introduce small, random delay after processing each message
            # This helps simulate human-like behavior
            await asyncio.sleep(random.uniform(0.1, 0.5))

            # Introduce delay after a batch of messages
            if messages_fetched_count % MESSAGE_BATCH_SIZE == 0:
                delay = random.uniform(MIN_MESSAGE_DELAY_SECONDS, MAX_MESSAGE_DELAY_SECONDS)
                logger.info(f"Processed {messages_fetched_count} messages. Waiting for {delay:.2f} seconds before next batch.")
                await asyncio.sleep(delay)

        # Save messages to data lake
        if messages_data:
            today_str = datetime.now().strftime('%Y-%m-%d')
            channel_messages_dir = os.path.join(RAW_MESSAGES_PATH, today_str, channel_name)
            os.makedirs(channel_messages_dir, exist_ok=True)

            output_file = os.path.join(channel_messages_dir, f"{channel_name}_{today_str}_{datetime.now().strftime('%H%M%S')}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(messages_data, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved {len(messages_data)} messages from '{entity.title}' to {output_file}")
        else:
            logger.info(f"No new messages found or scraped for '{entity.title}'.")

        return {
            'channel_url': channel_url,
            'channel_id': entity.id,
            'channel_title': entity.title,
            'messages_count': len(messages_data),
            'images_downloaded_count': len(downloaded_images),
            'status': 'success'
        }

    except FloodWaitError as e:
        # Increase the wait time slightly beyond Telegram's request
        wait_time = e.seconds + random.uniform(5, 15) # Add a random buffer
        logger.warning(f"FloodWaitError for {channel_url}: Must wait {e.seconds} seconds. Actual wait: {wait_time:.2f} seconds. Skipping for now.")
        await asyncio.sleep(wait_time) # Ensure the client waits here
        return {
            'channel_url': channel_url,
            'status': 'flood_wait',
            'error': str(e),
            'wait_seconds': wait_time
        }
    except SessionPasswordNeededError:
        logger.error("Session password needed. Please ensure you are logged in correctly if this is a private channel.")
        return {
            'channel_url': channel_url,
            'status': 'error',
            'error': 'Session password needed'
        }
    except PhoneNumberBannedError as e:
        logger.critical(f"FATAL: The phone number used for Telegram API has been banned. Error: {e}")
        # Here you might want to stop the whole process or signal for manual intervention
        raise # Re-raise to stop further scraping attempts with a banned number
    except Exception as e:
        logger.error(f"Error scraping channel {channel_url}: {e}", exc_info=True)
        return {
            'channel_url': channel_url,
            'status': 'error',
            'error': str(e)
        }

async def main():
    """Main function to run the scraping process for all channels."""
    if not API_ID or not API_HASH:
        logger.error("TELEGRAM_API_ID or TELEGRAM_API_HASH environment variables are not set. Please check your .env file.")
        return

    # Use os.path.join for the session file path, relative to where the script runs,
    # or better, mount a volume for it in Docker.
    # The session file will be created/accessed in the root of your project
    # if you run this from (venv) D:\Project\telegram_data_pipeline>
    session_file_path = os.path.join(os.getcwd(), SESSION_NAME) # This will create .session in D:\Project\telegram_data_pipeline\

    client = TelegramClient(session_file_path, API_ID, API_HASH)

    try:
        logger.info("Connecting to Telegram...")
        # Use async with for the client to ensure proper connection/disconnection
        async with client:
            if not await client.is_user_authorized():
                logger.info("Client not authorized. Sending authentication code...")
                try:
                    phone_number = input('Enter your phone number (e.g., +2519...): ')
                    await client.send_code_request(phone=phone_number)
                    # Add a slight delay after sending code request
                    await asyncio.sleep(random.uniform(2, 5)) 

                    code = input('Enter the code: ')
                    await client.sign_in(phone=phone_number, code=code)
                except SessionPasswordNeededError:
                    await client.sign_in(password=input('Two-step verification enabled. Please enter your password: '))
                except PhoneNumberBannedError as e:
                    logger.critical(f"FATAL: The phone number you entered is banned. Cannot proceed. Error: {e}")
                    return # Exit the main function if phone number is banned
                except Exception as e:
                    logger.critical(f"Authentication failed: {e}", exc_info=True)
                    return # Exit on other auth errors

            logger.info("Successfully authorized.")

            results = []
            for channel_url in TELEGRAM_CHANNELS:
                logger.info(f"Starting scrape for {channel_url}...")
                result = await scrape_channel(client, channel_url)
                results.append(result)
                
                # Introduce a significant, random delay between processing different channels
                delay_between_channels = random.uniform(MIN_CHANNEL_DELAY_SECONDS, MAX_CHANNEL_DELAY_SECONDS)
                logger.info(f"Finished scraping {channel_url}. Waiting for {delay_between_channels:.2f} seconds before next channel.")
                await asyncio.sleep(delay_between_channels) 

            logger.info("\n--- Scraping Summary ---")
            for res in results:
                logger.info(f"Channel: {res.get('channel_title', res.get('channel_url'))} - Status: {res['status']} - Messages: {res.get('messages_count', 0)} - Images: {res.get('images_downloaded_count', 0)}")

    except PhoneNumberBannedError:
        # This will catch the re-raised error from scrape_channel and prevent the finally block
        # from trying to disconnect a client that might be in a bad state from the ban
        logger.critical("Scraping terminated due to a banned phone number. Please replace the number.")
    except Exception as e:
        logger.critical(f"Fatal error during Telegram scraping process: {e}", exc_info=True)
    finally:
        # The `async with client:` block handles disconnection automatically.
        # This `finally` block is mostly for logging remaining cleanup if needed.
        logger.info("Scraping process concluded.")


if __name__ == '__main__':
    # Telethon requires asyncio to run.
    asyncio.run(main())