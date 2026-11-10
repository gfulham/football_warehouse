SELECT  
YEAR(WEEK_DATE_SUNDAY::DATE) AS YEAR,
WEEK_DATE_SUNDAY,
WEEK_NUMBER,
POSITION,
PLAYER as PLAYER_NAME,
TEAM,
LOWER(
        TRIM(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    PLAYER,
                    '\\b(Jr\\.?|Sr\\.?|II|III|IV|V)\\b',
                    '',
                    1, 0, 'i'
                ),
                '[^A-Za-z ]',
                ''
            )
        )
    ) AS PLAYER_NAME_CLEAN,
CAST (POINTS AS NUMBER) AS PROJECTION,
CAST (SD_PTS AS NUMBER) AS SD_PTS, 
CAST (FLOOR AS NUMBER) AS FLOOR,
CAST (CEILING AS NUMBER) AS CEILING,
CAST (UNCERTAINTY AS NUMBER) AS UNCERTAINTY,
from {{ source('raw','ffa_projections') }}
WHERE POSITION IN ('QB', 'RB', 'WR', 'TE', 'DST')