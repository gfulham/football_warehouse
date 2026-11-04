"""
Steps in this script:
1. Connect to Snowflake
2. Create the table if it doesn't exist
3. Get the existing weeks from the table
4. Get the available weeks from the data directory
5. Compare the two sets to find missing weeks
6. For each missing week, read the corresponding CSV file and upload it to Snowflake
"""

import snowflake.connector
import glob
import pandas as pd
import pathlib as pl
import os
from pathlib import Path
from snowflake.connector.pandas_tools import write_pandas
import re
import sys

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.DK_SALARIES (
        POSITION VARCHAR,
        NAME_ID VARCHAR,
        NAME VARCHAR,
        ID VARCHAR,
        ROSTER_POSITION VARCHAR,
        SALARY VARCHAR,
        GAME_INFO VARCHAR,
        TEAMABBREV VARCHAR,
        AVGPOINTSPERGAME VARCHAR,
        STATUS VARCHAR
    );
""")

print(cursor.fetchone())
# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")

existing_weeks = pd.read_sql("""
    SELECT DISTINCT
        TO_CHAR(
            TO_DATE(
                REGEXP_SUBSTR("GAME_INFO", '[0-9]{2}/[0-9]{2}/[0-9]{4}'), 
                'MM/DD/YYYY'    
            ),
            'YYYY-MM-DD'
        ) AS WEEK
    FROM 
    FANTASY_FOOTBALL.RAW.DK_SALARIES
    """, conn)

# change to a set for later comparison
existing_weeks_set = set(existing_weeks["WEEK"])
print("Existing weeks set:")
print(existing_weeks_set)

if existing_weeks.empty:
    print("No existing weeks found in the database.")
    # end the script if there are no existing weeks
    sys.exit()  # Terminating the script with an error code

Current_path = Path.cwd()
#print(Current_path)
Current_path = Current_path.parent
#print(Current_path)

data_dir = Current_path / "data" / "contest_salaries_draftkings"

files = glob.glob(f"{data_dir}\\DKSalaries*.csv")

available_weeks = set()
#
for file_path in files:
    #print(file_path)
    nfl_date = file_path.split("\\")[-1].split("_")[-1].split(".csv")[0]
    #print(nfl_date)
    available_weeks.add(nfl_date)
    
print("Weeks available:")
print(available_weeks)
#
missing_weeks = available_weeks - existing_weeks_set
print("Missing weeks:")
print(missing_weeks)



print(cursor.fetchall())

for week in missing_weeks:
    file_path = f"{data_dir}\\DKSalaries_{week}.csv"
    df = pd.read_csv(file_path)

    df.columns = (
        df.columns
        .str.replace("+", "", regex=False)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.upper()
    )

    print(f"Uploading {file_path} to Snowflake...")

    success, nchunks, nrows, output = write_pandas(
        conn,
        df,
        table_name="DK_SALARIES",
        database="FANTASY_FOOTBALL",
        schema="RAW",
        auto_create_table=False,
        overwrite=False
    )

    print(f"Success: {success}")    
    print(f"Rows loaded: {nrows}")
