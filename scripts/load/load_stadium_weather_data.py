import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

Current_path = Path.cwd()
Current_path = Current_path.parent
data_dir = Current_path / "data" 

city_geolocation_df = pd.read_csv(f"{data_dir}\\weather\\nfl_stadium_city_coordinates_2026.csv")
all_stadium_weather = []

BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_JEY = os.getenv("WEATHER_API_KEY")

for index, city in city_geolocation_df.iterrows():

    params = {
        "latitude": city["lat"],
        "longitude": city["long"],
        "hourly": "temperature_2m,precipitation_probability,precipitation,wind_speed_10m",
        "forecast_days": 7,
        "timezone": "auto",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "precipitation_unit": "inch"
    }

    response = requests.get(BASE_URL, params=params)

    data = response.json()

    #print(data)
    all_stadium_weather.append({
        "city": city["city"],
        "state": city["state"],
        "lat": city["lat"],
        "long": city["long"],
        "weather": data,
    })
    
dfs = []

for data in all_stadium_weather:
    df = pd.DataFrame(data["weather"]['hourly'])
    
    df["city"] = data['city']
    df["state"] = data['state']
    df["latitude"] = data["lat"]
    df["longitude"] = data["long"]
    
    dfs.append(df)

weather_df = pd.concat(dfs, ignore_index=True)

weather_df['time'] = pd.to_datetime(weather_df['time'])
weather_df['date'] = pd.to_datetime(weather_df['time']).dt.date
weather_df['time'] = weather_df['time'].dt.strftime("%H-%M-%S")

today = datetime.today()
today = today.strftime("%Y-%m-%d-%H-%M-%S")

weather_df.columns = weather_df.columns.str.upper()

weather_df.to_csv(f"{data_dir}\\weather\\nfl_stadium_weather_{today}.csv", index=False)
print("Saved wather data to csv ")

###### LOAD DATAFRAME TO SNOWFLAKE 
conn = snowflake.connector.connect(
    connection_name="whatever"
)
cursor = conn.cursor()

# test conneciton
cursor.execute("SELECT CURRENT_VERSION()")
print(cursor.fetchone())

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

success, nchunks, nrows, output = write_pandas(
            conn,
            weather_df,
            table_name="WEATHER",
            database="FANTASY_FOOTBALL",
            schema="RAW",
            auto_create_table=False,
            overwrite=False
        )
print(f"Success: {success}")    
print(f"Rows loaded: {nrows}")


