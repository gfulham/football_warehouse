{{ config(materialized='table') }}

SELECT * FROM {{ ref('mart_player_historical') }}
WHERE WEEK = (
    SELECT MAX(WEEK)
    FROM {{ ref('mart_player_historical') }}
)
