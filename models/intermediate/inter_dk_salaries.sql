SELECT 
dt.team,
dks.*
FROM 
{{ ref('stg_dk_salaries') }} dks

LEFT JOIN {{ ref('dim_nfl_teams') }} dt
    ON dt.team_ABBREVIATION = dks.team_abbreviation