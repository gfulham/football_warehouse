# This notebook will pull in weekly player data and load it into the snowflake database. 
# It will check for existing weeks and only pull in missing weeks.

import requests
import nflreadpy as nfl
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from datetime import datetime, date
import math

pd.set_option('display.max_rows', None)    # None removes the limit completely
pd.set_option('display.max_columns', None)

def get_current_football_week():
    # 1. Define the official kickoff date of Week 1 (Wednesday or Thursday)
    # The 2026 NFL regular season kicked off on Wednesday, Sept 9, 2026
    season_start_date = date(2026, 9, 9)
    
    # 2. Get today's date dynamically
    today = date.today()
    
    # 3. Handle out-of-season bounds
    if today < season_start_date:
        return "Preseason / Not Started"
        
    # Calculate how many days have elapsed since the start
    days_elapsed = (today - season_start_date).days
    
    # Each football week lasts 7 days (Thursday through Monday night games)
    # math.ceil ensures a Wednesday/Thursday reset starts the next week
    current_week = math.ceil((days_elapsed + 1) / 7)
    
    # 4. Cap at Week 18 (End of the regular season)
    if current_week > 18:
        return "Postseason / Regular Season Ended"
        
    return current_week

# Example Execution
#print(f"Today is {datetime.now().strftime('%A, %b %d, %Y')}")
#print(f"Current Football Week: {get_current_football_week()}")


# %%
conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

## %%
#columns = pd.read_sql("""
#    SELECT COLUMN_NAME
#    FROM FANTASY_FOOTBALL.INFORMATION_SCHEMA.COLUMNS
#    WHERE TABLE_SCHEMA = 'RAW'
#        AND TABLE_NAME = 'WEEKLY_PLAYER_STATS'
#    ORDER BY ORDINAL_POSITION
#""", conn)
#
#print(columns)
#
# %%
existing_weeks = pd.read_sql("""
    SELECT DISTINCT SEASON, WEEK
    FROM FANTASY_FOOTBALL.RAW.WEEKLY_PLAYER_STATS
""", conn)

#print("Existing weeks:")
#print(existing_weeks)

current_year = datetime.now().year
#print(f"Current Year: {current_year}")

# %%
# 2019–2021: Weeks 1–16
expected_2019_2021 = pd.MultiIndex.from_product(
    [range(2019, 2022), range(1, 18)],
    names=["SEASON", "WEEK"],
).to_frame(index=False)

# 2022–2025: Weeks 1–18
expected_2022_2025 = pd.MultiIndex.from_product(
    [range(2022, current_year), range(1, 19)],
    names=["SEASON", "WEEK"]
).to_frame(index=False)

# Current year: Weeks 1 through current week
expected_current = pd.MultiIndex.from_product(
    [[current_year], range(1, get_current_football_week() + 1)],
    names=["SEASON", "WEEK"]
).to_frame(index=False)

# Combine everything
expected_weeks = pd.concat(
    [expected_2019_2021, expected_2022_2025, expected_current],
    ignore_index=True
)

#print("Expected weeks:")
#print(expected_weeks)

missing = (
    pd.merge(
        expected_weeks,
        existing_weeks,
        on=["SEASON", "WEEK"],
        how="left",
        indicator=True
    )
)

# Missng years and weeks combination
missing = missing[missing["_merge"] == "left_only"]

missing_weeks = missing["WEEK"].tolist()
missing_seasons = missing["SEASON"].tolist()

player_stats = nfl.load_player_stats(missing_seasons, weeks=missing_weeks, stat_type='week')

ps_df = player_stats.to_pandas()
#ps_df.head()

ps_df.columns = ps_df.columns.str.upper()

ps_df.to_csv("weekly_player_stats.csv", index=False)

write_pandas(
    conn,
    ps_df,
    table_name = "WEEKLY_PLAYER_STATS",
    database="FANTASY_FOOTBALL",
    schema="RAW",
    #auto_create_table=True
)



