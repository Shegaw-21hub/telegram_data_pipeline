# D:\Project/telegram_data_pipeline/dbt_project/Dockerfile
FROM python:3.11-slim

WORKDIR /dbt_project

# Install system dependencies required by dbt-postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy dbt's specific requirements.txt and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual dbt project files from the build context's dbt_project directory
# into the container's WORKDIR (/dbt_project).
COPY ./ /dbt_project/ 

# Set DBT_PROFILES_DIR if profiles.yml is not in the default .dbt/ directory
ENV DBT_PROFILES_DIR=/dbt_project/

# Set the entrypoint to bash. Any commands passed to docker run/exec will then be run by bash.
ENTRYPOINT ["bash"]

# Set a default command to keep the container running indefinitely.
CMD ["-c", "dbt debug && sleep infinity"]