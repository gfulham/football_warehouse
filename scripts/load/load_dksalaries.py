import snowflake.connector
import glob

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

files = glob.glob(r"C:\Users\onlyu\OneDrive\Coding_Projects\Fantasy_Football\data\*DKSalaries*cleaned.csv")
#
for file_path in files:
    print(file_path)
    cursor.execute(f"PUT file://{file_path} @fantasy_football.raw.ffa_stage OVERWRITE = TRUE")

# See the staged files
print(cursor.execute("LIST @fantasy_football.raw.ffa_stage;").fetchall())

cursor.execute("""
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
""")

print(cursor.fetchall())



cursor.execute("""
    COPY INTO fantasy_football.raw.DK_SALARIES
    FROM @fantasy_football.raw.ffa_stage
    PATTERN = '.*DKSalaries.*'
    FILE_FORMAT = (
        TYPE = CSV 
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        )
    ON_ERROR = 'CONTINUE'
""")

print(cursor.fetchall())

