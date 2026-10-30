import snowflake.connector
import glob
import os

conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

#return the latest weather data file
files = glob.glob(r"C:\Users\onlyu\OneDrive\Coding_Projects\Fantasy_Football\data\nfl_stadium_weather_*.csv")
latest_file = max(files, key=lambda x: os.path.getctime(x))


cursor.execute(f"PUT file://{latest_file} @fantasy_football.raw.ffa_stage OVERWRITE = TRUE")

# See the staged files
print(cursor.execute("LIST @fantasy_football.raw.ffa_stage;").fetchall())

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_football.raw.weather (
        time VARCHAR,
        temperature_2m VARCHAR,
        precipitation_probability VARCHAR,
        precipitation VARCHAR,
        wind_speed_10m VARCHAR,
        city VARCHAR,
        state VARCHAR,
        latitude VARCHAR,
        longitude VARCHAR,
        date VARCHAR
    );
""")

print(cursor.fetchall())

cursor.execute("""
    COPY INTO fantasy_football.raw.weather
    FROM @fantasy_football.raw.ffa_stage
    PATTERN = '.*weather.*'
    FILE_FORMAT = (
        TYPE = CSV 
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        )
    ON_ERROR = 'CONTINUE'
""")

print(cursor.fetchall())