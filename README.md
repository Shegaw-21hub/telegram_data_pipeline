# 💊 Advanced Medical Telegram Analytics Pipeline

**Production-Grade Data Platform: Scraping → dbt Transformations → Analytics**  
[![dbt Tests](https://img.shields.io/badge/dbt_tests-100%25_passing-brightgreen)](https://github.com/Shegaw-21hub/telegram_data_pipeline/actions) 
[![Pipeline Coverage](https://img.shields.io/badge/coverage-Tasks_0-2_complete-blue)]()

<img src="docs/pipeline_architecture.png" width="700" alt="End-to-End Pipeline">



###  Enhanced dbt Transformations 
```sql
-- Example: dim_dates.sql (Full Time Dimension)
SELECT
    date_day as date_key,
    EXTRACT(YEAR FROM date_day) as year,
    EXTRACT(QUARTER FROM date_day) as quarter,
    TO_CHAR(date_day, 'Day') as day_name,
    -- 15+ additional time dimensions
FROM {{ dbt_utils.date_spine(
    datepart="day",
    start_date="cast('2023-01-01' as date)",
    end_date="cast('2025-12-31' as date)"
) }}
```
## 📚 Comprehensive Documentation
```
docs/
├── ONBOARDING.md          # Step-by-step setup
├── DATA_DICTIONARY.md     # Schema details
├── SCRAPING_GUIDE.md      # Channel list & schedules
└── TRANSFORMATION_SPEC.md # dbt model specifications
```
## 🛠️ Complete Installation Guide
### 1. Infrastructure Setup
```
# Clone with all dbt modules
git clone --recurse-submodules https://github.com/Shegaw-21hub/telegram_data_pipeline.git

# Initialize environment
docker-compose up -d postgres dbt-docs
```
### 2. Data Pipeline Execution
#### Load sample data (included in repo)
make seed-database

#### Run full transformation
docker-compose run dbt run --vars '{"full_refresh":true}'

#### View dbt docs
open http://localhost:8080
## 🔍 Verification Checklist
| Requirement             | Verification Method       | Status       |
|-------------------------|---------------------------|--------------|
| dbt models complete     | dbt test --store-failures | ✅ 12/12     |
| Raw data partitioned    | tree data/raw             | ✅ YYYY-MM-DD |
| Documentation exists    | ls docs/*.md              | ✅ 4 files   |
| CI/CD pipeline active   | GitHub Actions badge      | ✅ Passing   |

## 📈 Enhanced Data Model

![Enhanced Model](images/enhanced_model.png)

## 🧪 Testing Framework
### 1. Data Quality Tests
```$ dbt test
12 tests completed:
✔ 5 not_null tests (critical fields)
✔ 4 unique tests (primary keys)
✔ 3 custom SQL validations
```
### 2. Example Custom Test
-- tests/validate_message_dates.sql
SELECT message_id 
FROM {{ ref('fct_messages') }}
WHERE message_date > CURRENT_DATE  # Future dates invalid
## 📝 Updated Project Structure
```
.
├── dbt_medical/               # Full dbt project
│   ├── models/
│   │   ├── staging/           # 3 cleaned models
│   │   ├── marts/             # 5 dimensional models
│   │   └── utils/             # Macros
│   ├── tests/                 # 12+ tests
│   └── dbt_project.yml        # Configured packages
├── samples/                   # Example outputs
│   ├── raw_message.json       # Input sample
│   └;-> mart_output.csv       # Transformed sample
└── Makefile                   # Automated workflows
```
## ✉️ **Contact**

**Name:** Shegaw Adugna

**Email:** [shegamihret@gmail.com](mailto:shegamihret@gmail.com)

**GitHub:** [https://github.com/Shegaw-21hub/telegram_data_pipeline](https://github.com/Shegaw-21hub/telegram_data_pipeline)
