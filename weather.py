import requests
import os
from datetime import datetime
import tweepy
import logging

'''Importing API Tokens using file
Environment variables can be used. OS module is already imported for that functionality'''

keys = open('apitokens', 'r').read().splitlines()

'''Setup Twitter'''

api_key = keys[1]
api_secret = keys[2]
access = keys[3]
access_secret = keys[4]

authenticator = tweepy.OAuth1UserHandler(api_key, api_secret)
authenticator.set_access_token(access, access_secret)

api = tweepy.API(authenticator, wait_on_rate_limit=True)

'''Setup OpenWeather API'''

user_api = keys[7]
location = "BANGALORE"

complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api
api_link = requests.get(complete_api_link)
api_data = api_link.json()

'''Assigning variables for weather output'''

temp_city = ((api_data['main']['temp']) - 273.15)
weather_desc = api_data['weather'][0]['description']
hmdt = api_data['main']['humidity']
wind_spd = api_data['wind']['speed']
date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

'''Creating temp file to store weather data temporarily'''

with open('x0samnan.txt', 'w') as f:
    l2 = ("Weather Stats for - {}  || {}".format(location.upper(), date_time))
    l4 = "Current temperature is: {:.2f} deg C".format(temp_city)
    l5 = "Current weather description  :", weather_desc
    l6 = "Current Humidity      :", hmdt, '%'
    l7 = "Current wind speed    :", wind_spd, 'kmph'

    f.write(str(l2) + '\n')
    f.write(str(l4) + '\n')
    f.write(str(l5) + '\n')
    f.write(str(l6) + '\n')
    f.write(str(l7) + '\n')
    f.close()

'''Posting the weather information in twitter'''

logging.info("Tweeting the weather")
with open('x0samnan.txt', 'r') as f:
    api.update_status(f.read())

print("Successfully tweeted current weather information of", location)
