
import requests
import pandas as pd
from datetime import datetime

city_geolocation_df = pd.read_csv("C:\\Users\\onlyu\\OneDrive\\Coding_Projects\\Fantasy_Football\\data\\nfl_stadium_city_coordinates_2026.csv")

all_stadium_weather = []

API_KEY = "5ecdd6fd1b07f856442a0fb8d19ffbb7"
url = "https://api.open-meteo.com/v1/forecast"

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

    response = requests.get(url, params=params)

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

weather_df.to_csv(f"C:\\Users\\onlyu\\OneDrive\\Coding_Projects\\Fantasy_Football\\data\\nfl_stadium_weather_{today}.csv", index=False)
