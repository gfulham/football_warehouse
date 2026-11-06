SELECT  
TO_CHAR(
        TO_DATE(
            REGEXP_SUBSTR("GAME_INFO", '[0-9]{2}/[0-9]{2}/[0-9]{4}'), 
            'MM/DD/YYYY'    
        ),
        'YYYY-MM-DD'
    ) AS WEEK,
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
TEAMABBREV AS TEAM,
CAST(SALARY AS NUMBER) AS SALARY,
GAME_INFO,
STATUS
from {{ source('raw','dk_salaries') }}