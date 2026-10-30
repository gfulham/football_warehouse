SELECT 
    ROW_NUMBER() OVER (ORDER BY Team) AS team_key,
    *
    FROM {{ source('raw', 'nfl_teams') }}