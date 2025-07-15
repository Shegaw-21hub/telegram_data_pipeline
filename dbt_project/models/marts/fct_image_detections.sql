-- dbt/models/marts/fct_image_detections.sql
{{
  config(
    materialized='table'
  )
}}

SELECT
    d.detection_id,
    m.message_key,
    d.class_id,
    d.class_name,
    d.confidence,
    d.bbox,
    CASE 
        WHEN d.class_name IN ('pill', 'medicine', 'bottle') THEN 'medical'
        ELSE 'other'
    END as detection_category
FROM {{ source('raw', 'image_detections') }} d
LEFT JOIN {{ ref('fct_messages') }} m ON d.message_id = m.message_id