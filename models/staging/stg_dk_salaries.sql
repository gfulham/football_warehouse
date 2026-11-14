SELECT 
YEAR(WEEK) AS YEAR,
WEEK,
WEEKISO(WEEK) - 36 AS WEEK_NUMBER,
POSITION,
TRIM(NAME) AS NAME,
LOWER(
        TRIM(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    NAME,
                    '\\b(Jr\\.?|Sr\\.?|II|III|IV|V)\\b',
                    '',
                    1, 0, 'i'
                ),
                '[^A-Za-z ]',
                ''
            )
        )
    ) AS PLAYER_NAME_CLEAN,
ID AS DK_ID,
ROSTER_POSITION,
TEAMABBREV AS TEAM_ABBREVIATION,
CAST(SALARY AS NUMBER) AS SALARY,
GAME_INFO,
STATUS 
FROM (
    SELECT *,
        TO_DATE(
            REGEXP_SUBSTR("GAME_INFO", '[0-9]{2}/[0-9]{2}/[0-9]{4}'), 
            'MM/DD/YYYY'    
        ) AS WEEK
    FROM {{ source('raw','dk_salaries') }}
)


