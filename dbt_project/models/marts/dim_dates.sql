-- dbt/models/marts/dim_dates.sql
{{
  config(
    materialized='table'
  )
}}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2030-12-31' as date)"
    ) }}
)

SELECT
    date_day as date,
    EXTRACT(YEAR FROM date_day) as year,
    EXTRACT(MONTH FROM date_day) as month,
    EXTRACT(DAY FROM date_day) as day,
    EXTRACT(QUARTER FROM date_day) as quarter,
    EXTRACT(DOW FROM date_day) as day_of_week,
    EXTRACT(DOY FROM date_day) as day_of_year,
    CASE 
        WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE 
        ELSE FALSE 
    END as is_weekend
FROM date_spine