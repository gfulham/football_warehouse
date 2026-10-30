{{ config(materialized='table') }}

SELECT
    DIM_PLAYER.player_key,
    DIM_PLAYER.player_name_clean,
    STG_DK_SALARIES.salary,
    STG_DK_SALARIES.week,
    STG_DK_SALARIES.GAME_INFO,
    STG_FFA_PROJECTIONS.PROJECTION,
    STG_FFA_PROJECTIONS.SD_PTS,
    STG_FFA_PROJECTIONS.FLOOR,
    STG_FFA_PROJECTIONS.CEILING,
    STG_FFA_PROJECTIONS.UNCERTAINTY

FROM {{ ref('dim_player') }}

JOIN {{ ref('stg_dk_salaries') }}
    ON DIM_PLAYER.dk_id = STG_DK_SALARIES.DK_ID

JOIN {{ ref('stg_ffa_projections') }}
    ON DIM_PLAYER.player_name_clean = STG_FFA_PROJECTIONS.player_name_clean
