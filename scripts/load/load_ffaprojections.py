"""
Steps in the script:
1. Connect to Snowflake
2. Create the table if it doesn't exist
3. Get the existing weeks from the table
4. Get the available weeks from the data directory
5. Compare the two sets to find missing weeks
6. Add a date and week column to the dataframe if they don't exist
7. For each missing week, read the corresponding CSV file and upload it to Snowflake
"""

############## IMPORTS ##############
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import glob
from pathlib import Path
import pandas as pd

############### CONNECT TO SNOWFLAKE ##############
conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

################ CREATE TABLE IF NOT EXISTS ##############
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.ffa_projections (
        week_date_sunday VARCHAR,
        week_number VARCHAR,
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
""")
# test conneciton
print(cursor.fetchone())
################# GET EXISTING WEEKS FROM THE TABLE ##############
existing_weeks = pd.read_sql("""
    SELECT DISTINCT
        week_date_sunday
    FROM 
    FANTASY_FOOTBALL.RAW.FFA_PROJECTIONS
    """, conn)

existing_weeks_set = set(existing_weeks["WEEK_DATE_SUNDAY"])
print("Existing weeks set:")
print(existing_weeks_set)

################# GET AVAILABLE WEEKS FROM THE DATA DIRECTORY ##############
Current_path = Path.cwd()
Current_path = Current_path.parent
data_dir = Current_path / "data" / "projections" / "ffa"
files = glob.glob(str(data_dir) + "\\ffa_weekly_projections_*.csv")

available_weeks = set()

for file in files:
    #print(f"Found file: {file}")
    nfl_week = file.split("\\")[-1].split("_")[-1].split(".csv")[0]
    available_weeks.add(nfl_week)
    
print("Available weeks set:")
print(available_weeks)

#### COMPARE WEEKS IN DATABASE VS AVAILABLE LOCALLY ####

missing_weeks = available_weeks - existing_weeks_set
print(f"Missing weeks: {missing_weeks}")

#### LOOP THROUUGH FILES OF MISSING WEEKS, CLEAN, AND LOAD TO SNOWFLAKE DB

for week in missing_weeks:
    file_path = f"{data_dir}\\ffa_weekly_projections_{week}.csv"
    
    df = pd.read_csv(file_path)
    relative_path = file_path.split("\\")[-1]   
    print(f"Processing file: {relative_path}")
    if "week_date_sunday" in df.columns:
        print(f"File with date column: {relative_path}")
    else:
        date = file_path.split("ffa_weekly_projections_")[-1].split(".csv")[0]
        #date = datetime.datetime.strptime(date, "%Y_%m_%d").date()
        week_number = pd.to_datetime(date).week - 36
        print(f"Date: {date}, week: {week_number}")
        
        df["week_date_sunday"] = date
        df['week_number'] = week_number
        
        df = df[["week_date_sunday", "week_number"] + [c for c in df.columns if c not in ["week_date_sunday", "week_number"]]]
        # snowflake doesn't like spaces in column names, so we need to replace them with underscores
        df.columns = df.columns.str.strip().str.upper()
        #file_path = file_path.split(".csv")[0]
        #df.to_csv(file_path + "_cleaned.csv", index=False)
        #print(df.head())

        # break  # Remove this line if you want to process all files

        success, nchunks, nrows, output = write_pandas(
            conn,
            df,
            table_name="FFA_PROJECTIONS",
            database="FANTASY_FOOTBALL",
            schema="RAW",
            auto_create_table=False,
            overwrite=False
        )

        print(f"Success: {success}")    
        print(f"Rows loaded: {nrows}")

