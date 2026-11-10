# %% [markdown]
# This notebook will use the odds API to return odds for the NFL games

# %%
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
import requests
from datetime import datetime, timedelta
import json


# %%
BASE_URL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"

API_KEY = os.getenv("THE_ODDS_API_KEY")

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

games_data = response.json()

# Convert each game/event into a JSON string
records = [(json.dumps(item),) for item in games_data]

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


# %%
# load the df to snowflake
import snowflake.connector
import pandas as pd 

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

cursor.execute("""
    CREATE TABLE IF NOT EXISTS FANTASY_FOOTBALL.RAW.NFL_ODDS_JSON (
        INGESTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
        PAYLOAD VARIANT
    );
""")
# print create table response
print(cursor.fetchone())

# see the result of the CREATE TABLE statement
for record in records:
    cursor.execute("""
        INSERT INTO FANTASY_FOOTBALL.RAW.NFL_ODDS_JSON (PAYLOAD)
        SELECT PARSE_JSON(%s)
    """, record)

conn.commit()

# print the insert response from snowflake. 
print(cursor.fetchone())


