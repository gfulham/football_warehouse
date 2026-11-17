SELECT A.*
--CASE 
--    WHEN MARKET = 'h2h' AND PRICE < -120 THEN 'FAVORITE'
--    WHEN MARKET = 'h2h' AND PRICE >= -120 
--        AND MARKET = 'h2h' AND PRICE <= 120 THEN 'SPLIT'
--ELSE 'UNDERDOG'
--END AS TEAM_FAVORED  


FROM (
    SELECT DISTINCT
        PAYLOAD:id::VARCHAR AS GAME_ID,
        PAYLOAD:sport_title::VARCHAR AS SPORT,
        DATEADD(hour, -5, PAYLOAD:commence_time::VARCHAR) AS GAME_TIME,        
        PAYLOAD:home_team::VARCHAR AS TEAM,
        PAYLOAD:away_team::VARCHAR AS OPPONENT,
        'HOME' AS LOCATION,

        B.VALUE:key::VARCHAR AS BOOKMAKER,
        M.VALUE:key::STRING AS MARKET,
        O.VALUE:name::STRING AS OUTCOME,

        O.VALUE:point::FLOAT AS POINT,
        O.VALUE:price::FLOAT AS PRICE

    FROM {{ source('raw','nfl_odds_json') }},
    LATERAL FLATTEN(INPUT => PAYLOAD:bookmakers) B,
    LATERAL FLATTEN(INPUT => B.VALUE:markets) M,
    LATERAL FLATTEN(INPUT => M.VALUE:outcomes) O

    -- WHERE M.VALUE:key::VARCHAR = 'h2h'

) A

UNION ALL

SELECT A.*
--CASE 
--    WHEN MARKET = 'h2h' AND PRICE < -120 THEN 'FAVORITE'
--    WHEN MARKET = 'h2h' AND PRICE >= -120 
--        AND MARKET = 'h2h' AND PRICE <= 120 THEN 'SPLIT'
--    WHEN MARKET = 'h2h' AND PRICE > 120 THEN 'UNDERDOG'
--    ELSE 
--    NULL
--END AS TEAM_FAVORED  


FROM (
    SELECT DISTINCT
        PAYLOAD:id::VARCHAR AS GAME_ID,
        PAYLOAD:sport_title::VARCHAR AS SPORT,
        DATEADD(hour, -5, PAYLOAD:commence_time::VARCHAR) AS GAME_TIME,
        PAYLOAD:away_team::VARCHAR AS TEAM,
        PAYLOAD:home_team::VARCHAR AS OPPONENT,
        'HOME' AS LOCATION,

        B.VALUE:key::VARCHAR AS BOOKMAKER,
        M.VALUE:key::VARCHAR AS MARKET,
        O.VALUE:name::STRING AS OUTCOME,

        O.VALUE:point::FLOAT AS POINT,
        O.VALUE:price::FLOAT AS PRICE

    FROM {{ source('raw','nfl_odds_json') }},
    LATERAL FLATTEN(INPUT => PAYLOAD:bookmakers) B,
    LATERAL FLATTEN(INPUT => B.VALUE:markets) M,
    LATERAL FLATTEN(INPUT => M.VALUE:outcomes) O

) A

ORDER BY GAME_TIME DESC, TEAM, BOOKMAKER, MARKET, OUTCOME
