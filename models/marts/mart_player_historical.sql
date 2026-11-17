{{ config(materialized='table') }}

SELECT
    d.player_key,
    d.player_name_clean,
    dks.year,
    dks.week,
    dks.nfl_week_number,
    dks.team_abbreviation,
    dks.salary,
    dks.status,
    ffa.projection,
    fto.bookmaker,
    fto.location,
    fto.moneyline,
    fto.spread,
    fto.spread_odds,
    fto.over_under,
    fto.over_odds,
    fto.under_odds,
    fto.team_favored,
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

LEFT JOIN {{ ref('fact_team_odds') }} fto
    ON fto.nfl_week_number = dks.nfl_week_number
    AND fto.year = dks.year
    AND fto.TEAM_ABBREVIATION = dks.team_abbreviation




