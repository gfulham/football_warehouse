
CREATE TABLE IF NOT EXISTS fantasy_football.raw.ffa_projections (
    date VARCHAR,
    week VARCHAR,
    player VARCHAR,
    position VARCHAR,
    team VARCHAR,
    bye_week VARCHAR,
    points VARCHAR,
    sd_pts VARCHAR,
    dropoff VARCHAR,
    floor VARCHAR,
    ceiling VARCHAR,
    points_vor VARCHAR,
    floor_vor VARCHAR,
    ceiling_vor VARCHAR,
    rank VARCHAR,
    floor_rank VARCHAR,
    ceiling_rank VARCHAR,
    position_rank VARCHAR,
    tier VARCHAR,
    age VARCHAR,
    adp VARCHAR,
    aav VARCHAR,
    uncertainty VARCHAR,
    experience VARCHAR
);

CREATE TABLE IF NOT EXISTS fantasy_football.raw.dksalaries (
    date VARCHAR,
    week VARCHAR,
    Position VARCHAR,
    "Name + ID" VARCHAR,
    Name VARCHAR,
    ID VARCHAR,
    "Roster Position" VARCHAR,
    Salary VARCHAR,
    "Game Info" VARCHAR,
    TeamAbbrev VARCHAR,
    AvgPointsPerGame VARCHAR,
    Status VARCHAR
);

CREATE TABLE IF NOT EXISTS fantasy_football.raw.nfl_team_odds (
    date VARCHAR,
    week VARCHAR,
    Position VARCHAR,
    "Name + ID" VARCHAR,
    Name VARCHAR,
    ID VARCHAR,
    "Roster Position" VARCHAR,
    Salary VARCHAR,
    "Game Info" VARCHAR,
    TeamAbbrev VARCHAR,
    AvgPointsPerGame VARCHAR,
    Status VARCHAR
);

