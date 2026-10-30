SELECT  
CAST(date as DATE) as Date,
WEEK,
POSITION,
NAME,
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
"Roster Position" AS ROSTER_POSITION,
TEAMABBREV AS TEAM,
CAST(SALARY AS NUMBER) AS SALARY,
"Game Info" AS GAME_INFO,
STATUS
from {{ source('raw','dk_salaries') }}