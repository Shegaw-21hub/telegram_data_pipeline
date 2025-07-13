-- dbt/models/marts/fct_messages.sql
{{
  config(
    materialized='table'
  )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['message_id', 'channel_name']) }} as message_key,
    m.message_id,
    c.channel_key,
    d.date as date_key,
    m.message_text,
    m.view_count,
    m.has_media,
    m.media_type,
    m.media_path,
    LENGTH(m.message_text) as message_length,
    CASE 
        WHEN m.message_text ~* '(?i)\b(paracetamol|amoxicillin|insulin|ventolin)\b' THEN TRUE
        ELSE FALSE
    END as contains_drug_mention
FROM {{ ref('stg_telegram_messages') }} m
LEFT JOIN {{ ref('dim_channels') }} c ON m.channel_name = c.channel_name
LEFT JOIN {{ ref('dim_dates') }} d ON DATE(m.message_date) = d.date