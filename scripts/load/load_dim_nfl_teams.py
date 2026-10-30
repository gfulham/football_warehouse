import snowflake.connector
import glob

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

file_path = r"C:\Users\onlyu\OneDrive\Coding_Projects\Fantasy_Football\data\dim_nfl_teams.csv"

cursor.execute(f"PUT file://{file_path} @fantasy_football.raw.ffa_stage OVERWRITE = TRUE")

# See the staged files
print(cursor.execute("LIST @fantasy_football.raw.ffa_stage;").fetchall())

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.nfl_teams (
        Team VARCHAR,
        Abbreviation VARCHAR,
        City VARCHAR,
        State VARCHAR,
        Conference VARCHAR,
        Division VARCHAR
    );
""")

print(cursor.fetchall())

cursor.execute("""
    COPY INTO fantasy_football.raw.nfl_teams
    FROM @fantasy_football.raw.ffa_stage
    PATTERN = '.*nfl_teams.*'
    FILE_FORMAT = (
        TYPE = CSV 
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        )
    ON_ERROR = 'CONTINUE'
""")

print(cursor.fetchall())