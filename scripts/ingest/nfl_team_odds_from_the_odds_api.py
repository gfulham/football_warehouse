# %% [markdown]
# This notebook will use the odds API to return odds for the NFL games

# %%
import os
import requests

# %%
BASE_URL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"

API_KEY = "0052b4345f4731c48e71bd8f621c9c76"

query_params = {
    "oddsFormat": "american",
    #"sport_key": "americanfootball_nfl",
    "regions": "us",
    "apiKey": API_KEY
}

response = requests.get(BASE_URL, params=query_params)

print(response.status_code)
print(response.url)


if response.status_code == 200:
    print("Request successful")
    games_data = response.json()
    
else:
    raise ValueError(f"Request failed with status code {response.status_code}")

#print(response.json())


# %%
games_data = response.json()

#print(games_data[0])

#for sport in games_data:
#    print(sport["sport_key"], sport["sport_title"], sport["home_team"], sport["away_team"], sport["bookmakers"])

# %%
import pandas as pd

rows = []

for game in games_data:

    home_team = game["home_team"]
    away_team = game["away_team"]
    commence_time = game["commence_time"]

    for bookmaker in game["bookmakers"]:
        bookmaker_key = bookmaker["key"]
        last_update = bookmaker["last_update"]
        
        if bookmaker["key"] != "draftkings":
            continue

        for market in bookmaker["markets"]:

            if market["key"] != "h2h":
                continue

            outcomes = market["outcomes"]

            # Create dictionary: team -> odds
            odds = {
                outcome["name"]: outcome["price"]
                for outcome in outcomes
            }

            home_odds = odds[home_team]
            away_odds = odds[away_team]

            # Negative American odds = favorite
            if home_odds < 0:
                favored_team = home_team
                favorite_odds = home_odds
            else:
                favored_team = away_team
                favorite_odds = away_odds

            rows.append({
                "bookmaker" : bookmaker_key,
                "last_update": last_update,
                "commence_time": commence_time,
                "home_team": home_team,
                "away_team": away_team,
                "home_odds": home_odds,
                "away_odds": away_odds,
                "favored_team": favored_team,
                "favorite_odds": favorite_odds
            })

df = pd.DataFrame(rows)

df.head()
# %%
# get this upcoming sunday date
from datetime import datetime, timedelta

today = datetime.today()
upcoming_sunday = today + timedelta((6-today.weekday()) % 7)
#print(upcoming_sunday.strftime("%Y-%m-%d"))

week = pd.to_datetime(upcoming_sunday).week - 36
#print(week)

df["week_date"] = upcoming_sunday.strftime("%Y-%m-%d")
df["week_number"] = week

df = df[["week_date", "week_number"] + [c for c in df.columns if c not in ["week_date", "week_number"]]]

# %%
# add team abbreviations to df
team_abbreviations = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}

df["home_team_abbr"] = df["home_team"].map(team_abbreviations)
df["away_team_abbr"] = df["away_team"].map(team_abbreviations)
df.columns = df.columns.str.upper()

# Save theh dataframe to a csv, but just once a day. More frequent pulls will be saved to the snowflake db
data_folder = "C:\\Users\\onlyu\\OneDrive\\Coding_Projects\\Fantasy_Football\\data\\vegas_odds"
df.to_csv(f"{data_folder}/nfl_team_odds_{upcoming_sunday.strftime('%Y-%m-%d')}.csv", index=False)

# %%
# load the df to snowflake
import snowflake.connector
import glob
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd 

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.nfl_team_odds (
        WEEK_DATE VARCHAR,
        WEEK_NUMBER VARCHAR,	
        BOOKMAKER VARCHAR,
        LAST_UPDATE VARCHAR,
        COMMENCE_TIME VARCHAR,
        home_team VARCHAR,
        away_team VARCHAR,
        home_odds VARCHAR,
        away_odds VARCHAR,
        favored_team VARCHAR,
        favorite_odds VARCHAR,
        home_team_abbr VARCHAR,
        away_team_abbr VARCHAR
    );
""")
# see the result of the CREATE TABLE statement
print(cursor.fetchone())

write_pandas(
    conn,
    df,
    "NFL_TEAM_ODDS",
    database="FANTASY_FOOTBALL",
    schema="RAW"
)



