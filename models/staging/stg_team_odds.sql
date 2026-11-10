SELECT A.*,
CASE 
    WHEN TEAM_ODDS < -120 THEN 'FAVORITE'
    WHEN TEAM_ODDS >= -120 AND TEAM_ODDS <= 120 THEN 'SPLIT'
ELSE 'UNDERDOG'
END AS TEAM_FAVORED  


FROM (
    SELECT DISTINCT
        PAYLOAD:id::VARCHAR AS GAME_ID,
        PAYLOAD:sport_title::VARCHAR AS SPORT,
        DATEADD(hour, -5, PAYLOAD:commence_time::VARCHAR) AS GAME_TIME,        
        PAYLOAD:home_team::VARCHAR AS TEAM,
        PAYLOAD:away_team::VARCHAR AS OPPONENT,
        'HOME' AS LOCATION,

        B.VALUE:key::VARCHAR AS BOOKMAKER,
        --M.VALUE:key::VARCHAR AS MARKET,

        --O.VALUE:name::VARCHAR AS TEAM,
        --O.VALUE:price::NUMBER AS ODDS,
            CASE 
                WHEN M.VALUE:outcomes[0]:name::VARCHAR = PAYLOAD:home_team 
                THEN M.VALUE:outcomes[0]:price::NUMBER
                ELSE M.VALUE:outcomes[1]:price::NUMBER
            END AS TEAM_ODDS,
    


        M.VALUE:outcomes[0]:name::VARCHAR AS TEAN_1,
        M.VALUE:outcomes[0]:price::NUMBER AS TEAM_1_ODDS,
        M.VALUE:outcomes[1]:name::VARCHAR AS UNDERDOG_TEAM,
        M.VALUE:outcomes[1]:price::NUMBER AS UNDERDOG_ODDS
    FROM {{ source('raw','nfl_odds_json') }},
    LATERAL FLATTEN(INPUT => PAYLOAD:bookmakers) B,
    LATERAL FLATTEN(INPUT => B.VALUE:markets) M,
    LATERAL FLATTEN(INPUT => M.VALUE:outcomes) O

    WHERE M.VALUE:key::VARCHAR = 'h2h'

) A

UNION ALL

SELECT A.*,
CASE 
    WHEN TEAM_ODDS < -120 THEN 'FAVORITE'
    WHEN TEAM_ODDS >= -120 AND TEAM_ODDS <= 120 THEN 'SPLIT'
ELSE 'UNDERDOG'
END AS TEAM_FAVORED  


FROM (
    SELECT DISTINCT
        PAYLOAD:id::VARCHAR AS GAME_ID,
        PAYLOAD:sport_title::VARCHAR AS SPORT,
        DATEADD(hour, -5, PAYLOAD:commence_time::VARCHAR) AS GAME_TIME,
        PAYLOAD:away_team::VARCHAR AS TEAM,
        PAYLOAD:home_team::VARCHAR AS OPPONENT,
        'HOME' AS LOCATION,

        B.VALUE:key::VARCHAR AS BOOKMAKER,
        --M.VALUE:key::VARCHAR AS MARKET,

        --O.VALUE:name::VARCHAR AS TEAM,
        --O.VALUE:price::NUMBER AS ODDS,
            CASE 
                WHEN M.VALUE:outcomes[0]:name::VARCHAR = PAYLOAD:away_team 
                THEN M.VALUE:outcomes[0]:price::NUMBER
                ELSE M.VALUE:outcomes[1]:price::NUMBER
            END AS TEAM_ODDS,
    


        M.VALUE:outcomes[0]:name::VARCHAR AS TEAN_1,
        M.VALUE:outcomes[0]:price::NUMBER AS TEAM_1_ODDS,
        M.VALUE:outcomes[1]:name::VARCHAR AS UNDERDOG_TEAM,
        M.VALUE:outcomes[1]:price::NUMBER AS UNDERDOG_ODDS
    FROM {{ source('raw','nfl_odds_json') }},
    LATERAL FLATTEN(INPUT => PAYLOAD:bookmakers) B,
    LATERAL FLATTEN(INPUT => B.VALUE:markets) M,
    LATERAL FLATTEN(INPUT => M.VALUE:outcomes) O

    WHERE M.VALUE:key::VARCHAR = 'h2h'

) A

ORDER BY TEAM, BOOKMAKER
