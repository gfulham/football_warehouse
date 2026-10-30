-- CREATES A DIMENSION TABLE FOR PLAYERS
SELECT 
    ROW_NUMBER() OVER (ORDER BY DK_ID) AS player_key,
    NAME,
    DK_ID,
    player_name_clean 
    FROM {{ ref('stg_dk_salaries') }}