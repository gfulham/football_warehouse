# %% [markdown]
# This notebook will use the odds API to return odds for the NFL games

# %%
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import snowflake.connector
import pandas as pd 

################# REQUEST FROM THE ODDS API ############ 
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



############### LOAD TO SNOWFLAKE #######################
conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# TEST SF CONNECTION 
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

# CREATE TABLE IF NOT EXISTS
cursor.execute("""
    CREATE TABLE IF NOT EXISTS FANTASY_FOOTBALL.RAW.NFL_ODDS_JSON (
        INGESTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
        PAYLOAD VARIANT
    );
""")
print(cursor.fetchone())

# INSERT RAW JSON PAYLOAD INTO TABLE
for record in records:
    cursor.execute("""
        INSERT INTO FANTASY_FOOTBALL.RAW.NFL_ODDS_JSON (PAYLOAD)
        SELECT PARSE_JSON(%s)
    """, record)

conn.commit()
print(cursor.fetchone())


