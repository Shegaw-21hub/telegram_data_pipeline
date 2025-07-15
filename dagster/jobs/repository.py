# dagster/repository.py
from dagster import repository
from jobs.telegram_pipeline import telegram_pipeline

@repository
def telegram_repository():
    return [telegram_pipeline]