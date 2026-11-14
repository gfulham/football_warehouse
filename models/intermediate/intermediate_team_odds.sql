SELECT  
dt.TEAM_KEY,
stg_t.TEAM,
dt.TEAM_ABBREVIATION,
dt.CITY,
dt.STATE,
stg_t.LOCATION,
stg_t.GAME_ID,
stg_t.GAME_TIME,
YEAR(GAME_TIME) AS YEAR,
WEEKOFYEAR(DATEADD(day,-1, GAME_TIME)) -36 AS NFL_WEEK_NUMBER,
stg_t.OPPONENT,
stg_t.BOOKMAKER,
stg_t.TEAM_FAVORED,
stg_t.TEAM_ODDS
FROM
{{ ref('stg_team_odds') }} stg_t

LEFT JOIN {{ ref('dim_nfl_teams')}} dt 
    ON dt.team = stg_t.team
