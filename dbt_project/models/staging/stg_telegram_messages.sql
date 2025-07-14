-- dbt/models/staging/stg_telegram_messages.sql
{{
  config(
    materialized='view'
  )
}}

SELECT
    id as message_id,
    channel as channel_name,
    date::timestamp as message_date,
    message as message_text,
    views as view_count,
    media as has_media,
    media_type,
    media_path
FROM {{ source('raw', 'telegram_messages') }}
