-- dbt/tests/test_message_length_positive.sql
SELECT
    message_key,
    message_length
FROM {{ ref('fct_messages') }}
WHERE message_length < 0