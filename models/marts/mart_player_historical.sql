{{ config(materialized='table') }}

SELECT
    d.player_key,
    d.player_name_clean,
    dks.week,
    dks.week_number,
    dks.team,
    dks.salary,
    dks.status,
    ffa.projection,
    CASE
        WHEN dks.salary > 0
        THEN (ffa.projection / dks.salary) * 1000
        ELSE 0
    END AS PROJECTED_POINTS_PER_1K_SALARY
FROM 
    {{ ref('stg_dk_salaries') }} AS dks

JOIN {{ ref('dim_player') }} d 
    ON d.player_name_clean = dks.player_name_clean

LEFT JOIN {{ ref('stg_ffa_projections') }} ffa
    ON ffa.player_name_clean = dks.player_name_clean
    AND ffa.week_date_sunday = dks.week


