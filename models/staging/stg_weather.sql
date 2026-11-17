SELECT w.*,
dt.TEAM,
CASE
    WHEN dt.TEAM in (
        'ARIZONA CARDINALS',
        'ATLANTA FALCONS',
        'DALLAS COWBOYS',
        'HOUSTON TEXANS',
        'INDIANAPOLIS COLTS',
        'LAS VEGAS RAIDERS',
        'LOS ANGELES CHARGERS',
        'LOS ANGELES RAMS',
        'MINNESOTA VIKINGS',
        'DETRIOT LIONS',
        'NEW ORLEANS SAINTS'
    )
    THEN 'DOME'
    ELSE 'OPEN-AIR'
END AS STADIUM_TYPE
FROM {{ source('raw','weather')}} w
LEFT JOIN {{ref('dim_nfl_teams')}} dt
    ON dt.city = w.city


