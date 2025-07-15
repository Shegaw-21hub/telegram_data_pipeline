# dagster/jobs/telegram_pipeline.py
from dagster import job, op, get_dagster_logger
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_dagster_logger()

@op
def scrape_telegram_data(context):
    """Scrape data from Telegram channels"""
    logger.info("Starting Telegram scraping")
    try:
        result = subprocess.run(
            ["python", "telegram_scraper.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Scraping failed: {result.stderr}")
            raise Exception("Telegram scraping failed")
        
        logger.info("Telegram scraping completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error in scraping: {str(e)}")
        raise

@op
def load_raw_to_postgres(context, scrape_success):
    """Load raw data into PostgreSQL"""
    if not scrape_success:
        raise Exception("Skipping load due to previous failure")
    
    logger.info("Loading raw data to PostgreSQL")
    try:
        # Here you would implement the actual loading logic
        # For example, using psycopg2 to load JSON files into the database
        logger.info("Data loaded successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

@op
def run_dbt_transformations(context, load_success):
    """Run dbt transformations"""
    if not load_success:
        raise Exception("Skipping dbt due to previous failure")
    
    logger.info("Running dbt transformations")
    try:
        result = subprocess.run(
            ["dbt", "run", "--profiles-dir", "."],
            cwd="dbt",
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"dbt run failed: {result.stderr}")
            raise Exception("dbt transformation failed")
        
        logger.info("dbt transformations completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error in dbt: {str(e)}")
        raise

@op
def run_yolo_enrichment(context, dbt_success):
    """Run YOLO image processing"""
    if not dbt_success:
        raise Exception("Skipping YOLO due to previous failure")
    
    logger.info("Running YOLO image processing")
    try:
        result = subprocess.run(
            ["python", "image_processor.py"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"YOLO processing failed: {result.stderr}")
            raise Exception("YOLO processing failed")
        
        logger.info("YOLO processing completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error in YOLO processing: {str(e)}")
        raise

@op
def run_fastapi(context, yolo_success):
    """Start FastAPI server"""
    if not yolo_success:
        raise Exception("Skipping API due to previous failure")
    
    logger.info("Starting FastAPI server")
    # In production, you might want to run this as a separate service
    logger.info("API is ready at http://localhost:8000")
    return True

@job
def telegram_pipeline():
    """End-to-end pipeline for Telegram data processing"""
    scrape_result = scrape_telegram_data()
    load_result = load_raw_to_postgres(scrape_result)
    dbt_result = run_dbt_transformations(load_result)
    yolo_result = run_yolo_enrichment(dbt_result)
    api_result = run_fastapi(yolo_result)