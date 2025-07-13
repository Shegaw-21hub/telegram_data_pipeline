-- dbt/models/marts/dim_channels.sql
{{
  config(
    materialized='table'
  )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_key,
    channel_name,
    first_seen_date,
    last_seen_date,
    total_messages
FROM {{ ref('stg_telegram_channels') }}