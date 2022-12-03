from bs4 import BeautifulSoup
import requests as req
import pandas as pd

import datetime as dt
from datetime import datetime, date
from programs.keys import OpenWeather

today = date.today()
today = today.strftime("%Y%m%d")

lweek = date.today() - dt.timedelta(weeks=1)
lweek = lweek.strftime("%Y%m%d")

weather_codes = pd.read_csv('programs/wmo_codes.csv')
aqi_codes = pd.read_csv('programs/aqi_indices.csv')
cambridge_lat, cambridge_lon = 42.3736, -71.1097

def weather_aq_forecast(lat, lon):
    curr_weather = req.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=fahrenheit").json()['current_weather']
    weather_desc = weather_codes.loc[weather_codes['code'] == curr_weather['weathercode'], 'description']

    curr_aq = req.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OpenWeather.api_key}").json()['list'][0]
    aqi = curr_aq['main']['aqi']
    aqi_desc = aqi_codes.loc[aqi_codes['Index'] == aqi, 'Desc']

    data = {
        'Temperature': f"{curr_weather['temperature']}°F",
        'Weather': weather_desc.iloc[0],
        'Air Quality Index': aqi,
        'AQI_desc': aqi_desc.iloc[0],
        'Pollutants': [{'conc': val} for key, val in curr_aq['components'].items()]
        # 'Carbon Monoxide': f"{curr_aq['components']['co']}",
        # 'Nitrogen Dioxide': f"{curr_aq['components']['no2']} μg/m^3",
        # 'Ozone': f"{curr_aq['components']['o3']} μg/m^3",
        # 'PM 10': f"{curr_aq['components']['pm10']} μg/m^3",
        # 'PM 2.5': f"{curr_aq['components']['pm2_5']} μg/m^3"
    }
    return data

# print(weather_aq_forecast(cambridge_lat, cambridge_lon))