
# %%
# load the df to snowflake
import snowflake.connector
import glob

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())


# %%

files = glob.glob(r"C:\Users\onlyu\OneDrive\Coding_Projects\Fantasy_Football\data\vegas_odds\*nfl_team_odds*.csv")
#
for file_path in files:
    file_date = file_path.split("nfl_team_odds_")[-1].split(".")[0]
    
    
    print(file_path)
    cursor.execute(f"PUT file://{file_path} @fantasy_football.raw.ffa_stage OVERWRITE = TRUE")


# %%

# See the staged files
print(cursor.execute("LIST @fantasy_football.raw.ffa_stage;").fetchall())


# %%
cursor.execute("drop table if exists fantasy_football.raw.nfl_team_odds;")

print(cursor.fetchall())

# %%

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.nfl_team_odds (
        date VARCHAR,
        week VARCHAR,	
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

print(cursor.fetchall())


# %%

cursor.execute("""
    COPY INTO fantasy_football.raw.nfl_team_odds
    FROM @fantasy_football.raw.ffa_stage
    PATTERN = '.*nfl_team_odds.*'
    FILE_FORMAT = (
        TYPE = CSV 
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        )
    ON_ERROR = 'CONTINUE'
""")

print(cursor.fetchall())
