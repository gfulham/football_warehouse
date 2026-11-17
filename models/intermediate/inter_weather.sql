SELECT distinct
w.*,
o.game_time
FROM {{ref ('stg_weather')}} w
LEFT JOIN {{ref('stg_team_odds')}} o
    ON o.team = w.team
    AND w.date = TO_DATE(o.GAME_TIME)