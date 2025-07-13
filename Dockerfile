# D:\Project\telegram_data_pipeline\Dockerfile
FROM python:3.11-slim

# Set environment variables for non-secret paths within the container
# Secrets like API_ID/HASH/DB_PASS will be passed via docker-compose env_file
ENV DATA_LAKE_PATH=/app/data/raw
ENV LOGS_PATH=/app/logs
# Ensure consistent session name if not from .env
ENV TELEGRAM_SESSION_NAME=my_scraper_session

WORKDIR /app

# Install system dependencies required by psycopg2 (for PostgreSQL) and other libraries
# libpq-dev for PostgreSQL client development files
# gcc and python3-dev for compiling certain Python packages that require C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary application source code
# This assumes your Python code is in 'src/'
COPY src /app/src

# Create the data and logs directories inside the container,
# though volumes will typically overlay these. Good for consistency.
RUN mkdir -p ${DATA_LAKE_PATH} ${LOGS_PATH}

# Expose the port for FastAPI (if you're running it)
EXPOSE 8000

# Default command to run the FastAPI app (assuming it's in src/app/main.py)
# If you primarily run the scraper, you might change this or use separate entrypoints/commands in docker-compose.yml
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]