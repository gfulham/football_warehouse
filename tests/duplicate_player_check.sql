WITH duplicate_names AS (

    SELECT
    player_name_clean,
    week
    FROM {{ ref('stg_dk_salaries') }}
    GROUP BY player_name_clean, week
    HAVING COUNT(*) > 1

    UNION ALL

    SELECT
        player_name_clean,
        week
    FROM {{ ref('stg_ffa_projections') }}
    GROUP BY player_name_clean, week
    HAVING COUNT(*) > 1

)

SELECT *
FROM duplicate_names