import requests as req
import pandas as pd

from programs.keys import OpenWeather

# Reading in numeric codes and descriptions of weather and air quality for 
# more interpretable forecast results.
weather_codes = pd.read_csv('programs/wmo_codes.csv')
aqi_codes = pd.read_csv('programs/aqi_indices.csv')

def weather_aq_forecast(lat, lon):
    # Querying the Open-Meteo Weather Forecast API for the current weather
    # by user-determined location.
    curr_weather = req.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=fahrenheit").json()['current_weather']
    
    # Getting qualitative description that corresponds with the numeric 
    # World Meteorological Organization code from the API
    weather_desc = weather_codes.loc[weather_codes['code'] == curr_weather['weathercode'], 'description']

    # Getting quantitative air quality index and qualitative description for air quality
    curr_aq = req.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OpenWeather.api_key}").json()['list'][0]
    aqi = curr_aq['main']['aqi']
    aqi_desc = aqi_codes.loc[aqi_codes['Index'] == aqi, 'Desc']

    # Formatting the forecast data to display in EnviroHub's forecast format
    data = {
        'Temperature': f"{curr_weather['temperature']}°F",
        'Weather': weather_desc.iloc[0],
        'Air Quality Index': aqi,
        'AQI_desc': aqi_desc.iloc[0],
        'Pollutants': [{'conc': val} for key, val in curr_aq['components'].items()]
    }

    return data
