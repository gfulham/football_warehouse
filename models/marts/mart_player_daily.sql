{{ config(materialized='table') }}

SELECT * FROM {{ ref('mart_player_historical') }}
WHERE WEEK_NUMBER = (
    SELECT MAX(WEEK_NUMBER)
    FROM {{ ref('mart_player_historical') }}
)
