WITH all_players AS (

    SELECT PLAYER_NAME_CLEAN, POSITION
    FROM {{ ref('stg_ffa_projections') }}

    UNION

    SELECT PLAYER_NAME_CLEAN, POSITION
    FROM {{ ref('stg_dk_salaries') }}

)

SELECT
    ROW_NUMBER() OVER (ORDER BY PLAYER_NAME_CLEAN) AS PLAYER_KEY,
    PLAYER_NAME_CLEAN,
    POSITION
FROM all_players