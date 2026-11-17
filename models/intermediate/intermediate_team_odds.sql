SELECT  
    TEAM,
    OPPONENT,
    BOOKMAKER,
    LOCATION,
    GAME_ID,
    GAME_TIME,
    -- Moneyline
    MAX(CASE
        WHEN MARKET = 'h2h' AND OUTCOME = TEAM
        THEN PRICE
    END) AS MONEYLINE,

    -- Spread
    MAX(CASE
        WHEN MARKET = 'spreads' AND OUTCOME = TEAM
        THEN POINT
    END) AS SPREAD,

    MAX(CASE
        WHEN MARKET = 'spreads' AND OUTCOME = TEAM
        THEN PRICE
    END) AS SPREAD_ODDS,

    -- Over/Under
    MAX(CASE
        WHEN MARKET = 'totals' AND OUTCOME = 'Over'
        THEN POINT
    END) AS OVER_UNDER,

    MAX(CASE
        WHEN MARKET = 'totals' AND OUTCOME = 'Over'
        THEN PRICE
    END) AS OVER_ODDS,

    MAX(CASE
        WHEN MARKET = 'totals' AND OUTCOME = 'Under'
        THEN PRICE
    END) AS UNDER_ODDS

FROM 
    {{ ref('stg_team_odds') }}

GROUP BY
    TEAM,
    OPPONENT,
    BOOKMAKER,
    LOCATION,
    GAME_ID,
    GAME_TIME
