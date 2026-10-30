import requests

all_city_coordinates = []

#Get all city and state data for lat and long coordinates of the satdium
API_KEY = "5ecdd6fd1b07f856442a0fb8d19ffbb7"
url = "http://api.openweathermap.org/geo/1.0/direct"
cities = [
    ["Glendale", "Arizona", "US"],
    ["Atlanta", "Georgia", "US"],
    ["Baltimore", "Maryland", "US"],
    ["Orchard Park", "New York", "US"],
    ["Charlotte", "North Carolina", "US"],
    ["Chicago", "Illinois", "US"],
    ["Cincinnati", "Ohio", "US"],
    ["Cleveland", "Ohio", "US"],
    ["Arlington", "Texas", "US"],
    ["Denver", "Colorado", "US"],
    ["Detroit", "Michigan", "US"],
    ["Green Bay", "Wisconsin", "US"],
    ["Houston", "Texas", "US"],
    ["Indianapolis", "Indiana", "US"],
    ["Jacksonville", "Florida", "US"],
    ["Kansas City", "Missouri", "US"],
    ["Paradise", "Nevada", "US"],
    ["Inglewood", "California", "US"],
    ["Inglewood", "California", "US"],
    ["Miami Gardens", "Florida", "US"],
    ["Minneapolis", "Minnesota", "US"],
    ["Foxborough", "Massachusetts", "US"],
    ["New Orleans", "Louisiana", "US"],
    ["East Rutherford", "New Jersey", "US"],
    ["East Rutherford", "New Jersey", "US"],
    ["Philadelphia", "Pennsylvania", "US"],
    ["Pittsburgh", "Pennsylvania", "US"],
    ["Santa Clara", "California", "US"],
    ["Seattle", "Washington", "US"],
    ["Tampa", "Florida", "US"],
    ["Nashville", "Tennessee", "US"],
    ["Landover", "Maryland", "US"]
]

for each in cities:

    params = {
        "q": ",".join(each),
        "appid": API_KEY
    }

    response = requests.get(url, params=params)

    print(response.status_code)

    data=response.json()

    all_city_coordinates.append(data)

    for each in data:
        print(each['name'], each['lat'], each['lon'])
        
print(all_city_coordinates)

import pandas as pd

rows = []

for city in all_city_coordinates:
    for each in city:
        city = each["name"]
        state = each["state"]
        lat = each["lat"]
        long = each['lon']
        
        rows.append({
            "city" : city,
            "state": state, 
            "lat"  : lat,
            "long" : long
        })
    
df = pd.DataFrame(rows)

from datetime import datetime

today = datetime.today()
year = today.strftime("%Y")

data_folder = "C:\\Users\\onlyu\\OneDrive\\Coding_Projects\\Fantasy_Football\\data"

df.to_csv(f"{data_folder}/nfl_stadium_city_coordinates_{year}.csv", index=False)