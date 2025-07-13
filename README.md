# 🏥 Ethiopian Medical Telegram Analytics

**Tasks 0-2 Completed: Environment Setup • Data Scraping • dbt Modeling**  
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/) 
[![dbt 1.5](https://img.shields.io/badge/dbt-1.5-orange.svg)](https://www.getdbt.com/) 
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)

<img src="docs/interim_architecture.png" width="600" alt="Interim Architecture">

## ✅ Interim Deliverables Completed

### Task 0 - Project Setup
```bash
.
├── Dockerfile                  # Containerized Python+PostgreSQL
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── .gitignore                 # Excludes secrets/logs
```
### Task 1 - Data Scraping
### Key Features
## Features

- Scrapes 3+ Ethiopian medical channels (`Chemed`, `Lobelia`, `Tikvah`)
- Stores raw JSON in a partitioned structure:  
  `data/raw/telegram_messages/YYYY-MM-DD/<channel>.json`  
  _Example:_ `data/raw/telegram_messages/2024-07-10/chemed.json`
- Robust logging  
  _Log file:_ `scraping/scraper.log`


### Task 2 - dbt Modeling
## Star Schema Implemented

- `dim_channels` – Channel metadata  
- `dim_dates` – Time dimensions  
- `fct_messages` – Message facts (links to dims)

# 🛠️ Interim Setup Guide
### Prerequisites
- Docker Desktop
- Python 3.11
- Telegram API ID/HASH
##  Installation
## Clone, Setup, and Start Containers

```bash
# Clone the repository
git clone https://github.com/Shegaw-21hub/telegram_data_pipeline.git

# Navigate into the project directory
cd telegram_data_pipeline

# Copy environment configuration file and add your credentials
copy .env.example .env

# Start the PostgreSQL container
docker-compose up -d postgres
```

## Data Collection

```
python -m pip install -r requirements.txt
python scraping/telegram_scraper.py
```

## Run dbt Models
```bash
cd dbt_medical
dbt run --select staging+   # Builds all models in staging and downstream
dbt test                    # Runs 12+ tests (schema + data tests)
```
# 📊 Interim Data Model
<img src="docs/star_schema.png" width="400" alt="Star Schema">

# 🔍 Key Files for Grading
| Task | Critical Files                                                                 |
|------|----------------------------------------------------------------------------------|
| 0    | `Dockerfile`, `docker-compose.yml`, `.gitignore`                                |
| 1    | `scraping/telegram_scraper.py`, `data/raw/` structure                            |
| 2    | `dbt_medical/models/{staging,marts}/`, `dbt_medical/tests/`                      |

# 📝 Interim Report Highlights
## Highlights

- **Partitioned Data Lake**: Daily JSON files preserve raw data
- **dbt Tests**: 100% pass rate on primary keys and custom checks
- **Error Handling**: Scraper survives rate limits via exponential backoff

📌 *Full interim code available in the `main` branch*

**Contact:** Shegaw Adugna  
📧 [shegamihret@gmail.com](mailto:shegamihret@gmail.com)  
🔗 [GitHub Repository](https://github.com/Shegaw-21hub/telegram_data_pipeline)
