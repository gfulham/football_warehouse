{{ config(materialized='table') }}

SELECT
    DIM_PLAYER.player_key,
    DIM_PLAYER.player_name_clean,
    STG_DK_SALARIES.DK_ID,
    STG_DK_SALARIES.salary,
    STG_DK_SALARIES.week,
    STG_DK_SALARIES.team,
    STG_DK_SALARIES.position,
    STG_DK_SALARIES.GAME_INFO,
    STG_FFA_PROJECTIONS.PROJECTION,
    STG_FFA_PROJECTIONS.SD_PTS,
    STG_FFA_PROJECTIONS.FLOOR,
    STG_FFA_PROJECTIONS.CEILING,
    STG_FFA_PROJECTIONS.UNCERTAINTY,
    CASE
        WHEN STG_DK_SALARIES.salary > 0
        THEN (STG_FFA_PROJECTIONS.PROJECTION / STG_DK_SALARIES.salary) * 1000
        ELSE 0
    END AS PROJECTED_POINTS_PER_1K_SALARY

FROM {{ ref('dim_player') }}

JOIN {{ ref('stg_dk_salaries') }}
    ON DIM_PLAYER.dk_id = STG_DK_SALARIES.DK_ID
    AND STG_DK_SALARIES.WEEK = (
        SELECT MAX(WEEK)
        FROM {{ ref('stg_dk_salaries') }}
    )

JOIN {{ ref('stg_ffa_projections') }}
    ON DIM_PLAYER.player_name_clean = STG_FFA_PROJECTIONS.player_name_clean
    AND STG_FFA_PROJECTIONS.WEEK = (
        SELECT MAX(WEEK)
        FROM {{ ref('stg_ffa_projections') }}
    )

JOIN {{ ref('dim_nfl_teams') }}
    ON STG_DK_SALARIES.TeamAbbrev = DIM_NFL_TEAMS.Abbreviation

JOIN {{ ref('nfl_team_odds') }}
    ON dim_nfl_teams.abbrevuatiuon = DIM_PLAYER.player_name_clean
