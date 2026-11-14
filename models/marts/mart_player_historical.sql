{{ config(materialized='table') }}

SELECT
    d.player_key,
    d.player_name_clean,
    dks.year,
    dks.week,
    dks.week_number AS NFL_WEEK_NUMBER,
    dks.team_abbreviation,
    dks.salary,
    dks.status,
    ffa.projection,
    ito.location,
    ito.team_favored,
    ito.team_odds,
    CASE
        WHEN dks.salary > 0
        THEN (ffa.projection / dks.salary) * 1000
        ELSE 0
    END AS PROJECTED_POINTS_PER_1K_SALARY
FROM 
    {{ ref('inter_dk_salaries') }} dks

JOIN {{ ref('dim_player') }} d 
    ON d.player_name_clean = dks.player_name_clean

LEFT JOIN {{ ref('stg_ffa_projections') }} ffa
    ON ffa.player_name_clean = dks.player_name_clean
    AND ffa.week_date_sunday = dks.week

LEFT JOIN {{ ref('intermediate_team_odds') }} ito
    ON ito.nfl_week_number = dks.week_number
    AND ito.year = dks.year
    AND ito.TEAM_ABBREVIATION = dks.team_abbreviation


