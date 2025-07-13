-- dbt/models/staging/stg_telegram_channels.sql
 {{
  config(
    materialized='view'
  )
 }}

SELECT
    DISTINCT channel as channel_name,
    MIN(date::timestamp) as first_seen_date,
    MAX(date::timestamp) as last_seen_date,
    COUNT(*) as total_messages
FROM {{ source('raw', 'telegram_messages') }}
GROUP BY channel