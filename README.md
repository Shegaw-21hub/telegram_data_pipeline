# 🏥 Telegram Medical Analytics Pipeline

This project delivers an end-to-end data pipeline for processing Telegram data into an analytical API, focusing on pharmaceutical intelligence in Ethiopian medical channels.

**End-to-End Data Product: Scraping → ETL (dbt) → AI Enrichment (YOLOv8) → Analytics API (FastAPI) → Orchestration (Dagster)**

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/telegram-med-analytics-pipeline/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/telegram-med-analytics-pipeline/actions)

<img src="docs/screenshots/pipeline_architecture.png" width="600" alt="System Architecture">

A production-ready data pipeline analyzing Ethiopian medical Telegram channels for pharmaceutical intelligence, price trends, and counterfeit detection.

## 🚀 Key Features

-   **Telethon-powered scraping** of 10+ medical Telegram channels
-   **Modern ELT pipeline** with dbt (star schema optimized for analytics) - *Currently under active development for this interim.*
-   **AI-powered image recognition** using YOLOv8 (pills, syringes detection)
-   **Analytical API** with FastAPI (top products, price trends, visual content stats)
-   **Dagster-orchestrated** with error handling & daily schedules
-   **Infra-as-Code** via Docker & Terraform

## 📂 Repository Structure

```bash
.
├── pipelines/          # Core data workflows
│   ├── extraction/     # Telegram scrapers (Task 1)
│   ├── transformation/ # dbt models (Task 2 - In progress)
│   └── enrichment/     # YOLOv8 detection (Task 3 - Future)
├── services/           # API & orchestration (Tasks 4 & 5 - Future)
├── infra/              # Docker/Terraform configs (Task 0)
├── lib/                # Shared utilities
└── tests/              # Unit/integration/e2e
```
## 🛠️ Quick Start

This section guides you through setting up and running the core components of the pipeline.

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Telegram API credentials**  
  Obtain from [my.telegram.org](https://my.telegram.org)
## ⚙️ Installation & Initial Setup

Clone the repository:

```powershell
git clone https://github.com/Shegaw-21hub/telegram_data_pipeline.git
cd telegram_data_pipeline
## ⚙️ Installation & Initial Setup

This section guides you through setting up and running the core components of the pipeline.

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Telegram API credentials**  
  Obtain from [my.telegram.org](https://my.telegram.org)

### 🛠️ Step-by-Step Setup

```powershell
# Clone the repository
git clone https://github.com/Shegaw-21hub/telegram_data_pipeline.git
cd telegram_data_pipeline

# Duplicate .env file
cp .env.example .env

# Open .env and populate with your credentials:
# - TELEGRAM_API_ID
# - TELEGRAM_API_HASH
# - POSTGRES_USER
# - POSTGRES_PASSWORD
# - POSTGRES_DB
# These are securely loaded using python-dotenv and are ignored by Git (.gitignore)

# Start the PostgreSQL container
docker-compose up -d postgres
```
## Start Dockerized Services (Task 0 - Complete):

PowerShell

```powershell
docker-compose up -d --build
This command builds application and dbt images, and starts the PostgreSQL database, ensuring a reproducible and portable development environment. Verify `postgres_db` is healthy using `docker-compose ps`.

Crucially for Windows: Ensure your project's drive (e.g., `D:`) is correctly shared in Docker Desktop settings (`Settings -> Resources -> File Sharing`) for persistent data storage on the host.
```
### Running Key Pipeline Components
Execute Data Scraping (Task 1 - Complete):

PowerShell

```powershell
docker exec -it telegram_scraper_app python pipelines/extraction/telegram_scraper.p
```
**Note:** If encountering a `PhoneNumberBannedError`, ensure you use a new, unbanned Telegram phone number and delete any existing `.session` files from the `telegram_sessions` directory before re-running.

Upon successful completion, raw messages (JSON) and associated media will be stored in `data/raw/telegram_messages/` and `data/raw/telegram_images/` respectively, structured by date and channel name.
Execute Data Loading & Transformation (Task 2 - In Progress):

**Data Loading Script (Initial Phase of Task 2 - Implemented):**

Execute Data Loading & Transformation (Task 2 - In Progress):

**Data Loading Script (Initial Phase of Task 2 - Implemented):**

A Python script (`pipelines/ingestion/load_raw_data_to_db.py` — adjust path if different) is implemented to read the raw JSON files from the data lake and load them into a raw schema within the `postgres_db` database. This serves as the foundation for dbt transformations.

Execute it within the app container:

```bash
docker exec -it telegram_scraper_app python pipelines/ingestion/load_raw_data_to_db.py
```
## dbt Models & Transformation (Core of Task 2 - Under Development):

The dbt project (`pipelines/transformation/`) is initialized and connected to the PostgreSQL database, ready for transformation logic.

**Current Focus:**  
Developing comprehensive dbt models (`stg_*.sql`, `dim_*.sql`, `fct_*.sql`) for data cleaning, restructuring, and building the analytical star schema (`dim_channels`, `dim_dates`, `fct_messages`).

### Next Steps:

- Populating `stg_telegram_messages.sql` to clean and extract key fields from raw JSON.
- Building `dim_channels.sql` and `dim_dates.sql` for consistent dimensions.
- Developing `fct_messages.sql` to integrate message details and link to dimensions.
- Implementing robust data tests (`dbt test`) to ensure data quality and integrity at each transformation layer.
- Generating detailed dbt documentation (`dbt docs generate`) to provide clear data lineage and definitions.

These steps are crucial for transforming raw, messy data into a clean, trusted, and analytics-ready product.
# 🚀 Project Status: Interim Submission (Progress on Tasks 0, 1, & 2)

This section directly addresses the deliverables for the interim submission, outlining the current progress and a clear roadmap to meet all requirements.

## Complete GitHub Repository
This repository showcases the project's structure, Docker configurations, and the implemented data scraping functionality, providing a solid base for further development.

## Working Setup (Task 0 Complete)
- A robust and reproducible development environment is established using Docker and Docker Compose, enabling seamless setup on any compatible machine.
- Environment variables are securely managed, and essential `.gitignore` and `.dockerignore` configurations are in place for best practices.

## Data Lake with Raw Data (Task 1 Complete)
- The `pipelines/extraction/telegram_scraper.py` is fully operational, successfully extracting raw message data and associated media from specified Telegram channels.
- Raw data is systematically stored in a partitioned data lake structure (`data/raw/`), serving as the definitive source of truth.

## DBT Project & Data Transformation (Task 2 - In Progress)
- The initial phase of Task 2, which involves loading raw JSON data from the data lake into the PostgreSQL database, has been successfully implemented and verified. This establishes the necessary foundation for dbt.
- The dbt project is set up, demonstrating the understanding of dbt's role in creating a reliable "data factory."
- **Key Focus for Completion:**  
  The primary objective moving forward is the full implementation of dbt models (staging, mart), comprehensive testing (including custom data tests), and thorough documentation (`dbt docs generate`). This will ensure the transformation layer meets the highest standards of clarity, reliability, and analytical readiness for the final submission.

## 📊 Sample Analytics

PowerShell

```powershell
GET /api/analytics/top-products?limit=5


{
  "results": [
    {"product": "Paracetamol", "mentions": 142},
    {"product": "Amoxicillin", "mentions": 98}
  ]
}
```
## 🤝 Contributing

Fork the project

Create your feature branch (`git checkout -b feat/amazing-feature`)

Commit changes (`git commit -m 'Add amazing feature'`)

Push to branch (`git push origin feat/amazing-feature`)

Open a Pull Request

## ✉️ Contact

**Name:** Shegaw Adugna

**Email:** shegamihret@gmail.com

**GitHub:** [https://github.com/Shegaw-21hub/telegram_data_pipeline](https://github.com/Shegaw-21hub/telegram_data_pipeline)
