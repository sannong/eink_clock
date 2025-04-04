#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Basic clock with e-ink display and weather data
# Designed for Waveshare 2.13" e-ink display (V4) and Raspberry Pi Zero W
#
# The code is based on the Waveshare example code for the 2.13" e-ink display and the following reddit thread:
# https://www.reddit.com/r/raspberry_pi/comments/vi2xow/i_made_a_basic_clock_with_a_pi_zero_and_an_eink/?utm_source=share&utm_medium=web2x&context=3
#

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')   # path to the waveshare images/fonts
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')   # path to the waveshare  libraries
icondir = os.path.dirname(os.path.realpath(__file__))  # path to the meteocons font
if os.path.exists(libdir):
    sys.path.append(libdir)
print(libdir)
print(picdir)     
print(icondir)     
import requests
import logging
from waveshare_epd import epd2in13_V4
import time
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
from pprint import pprint
import dotenv 

# Load environment variables from .env file
# This contains the OpenWeatherMap API key
dotenv.load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")
zip_code = os.getenv("ZIP_CODE")
local = os.getenv("LOCAL")

# OpenWeatherMap API key and settings
# API reference: https://openweathermap.org/current
# Help/concept from: https://www.hackster.io/gatoninja236/real-time-weather-with-raspberry-pi-4-ad621f
settings = {
    'api_key':weather_api_key,
    'zip_code':zip_code,
    'country_code':local,
    'temp_unit':'imperial'} #unit can be metric, imperial, or kelvin
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"
weather_url = BASE_URL.format(settings["api_key"],settings["zip_code"],settings["country_code"],settings["temp_unit"])

# Map the OpenWeatherMap icon code to the appropriate font character
# Icon source: http://www.alessioatzeni.com/meteocons/ 
# Help/concept from: https://learn.adafruit.com/raspberry-pi-e-ink-weather-station-using-python/weather-station-code
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

font76 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 76)   
font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
icon_font = ImageFont.truetype(os.path.join(icondir, "meteocons.ttf"), 30)
    
logging.basicConfig(level=logging.DEBUG)

epd = epd2in13_V4.EPD()
print(epd.height)   #debugging purposes
print(epd.width)

# Weather data global variables
weather_data = None
temperature = None
weather_icon = None

#function to get the weather data from OpenWeatherMap API
def get_weather_data():
    weather_data = requests.get(weather_url).json()
    temperature = str(round(weather_data["main"]["temp"])) # temperature in Fahrenheit
    weather_icon = ICON_MAP[weather_data["weather"][0]["icon"]] # weather icon code

try:
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    # partial update
    logging.info("4.show time...")

    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_image2 = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.displayPartBaseImage(epd.getbuffer(time_image2))
    start_hour = datetime.now().hour
    
    # Get the weather data for the first time
    get_weather_data()
    pprint(weather_data)    # print to console just for information
        
    while (True):
          
        # Refresh the display every hour  
        if (start_hour != datetime.now().hour):
            start_hour = datetime.now().hour
            epd.Clear(0xFF)
            epd.displayPartBaseImage(epd.getbuffer(time_image2))
        
        #update weather every 10 minutes
        if (datetime.now().minute % 10 == 0):
            get_weather_data()
            
        dateStr = datetime.now().strftime('%m/%d') + " "
        tempStr = " " + temperature + "°F"
        iconStr = "   " + weather_icon 
        
        dateLen = time_draw.textlength(dateStr, font=font30)  
        tempLen = time_draw.textlength(tempStr, font=font30) 
        iconLen = time_draw.textlength(iconStr, font=icon_font)
            
        #time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)
        time_draw.text((125, 50), datetime.now().strftime('%H:%M'), font = font76, fill = 0, anchor="mm")
        time_draw.text((125 - dateLen, 122), dateStr, font = font30, fill = 0, anchor="ld")
        time_draw.text((125, 122), " - ", font = font30, fill = 0, anchor="md")
        time_draw.text((125 + tempLen, 122), tempStr, font = font30, fill = 0, anchor="rd")
        time_draw.text((125 + tempLen + iconLen, 122), iconStr, font = icon_font, fill = 0, anchor="rd")
        epd.displayPartial(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
        
        now = datetime.now()
        seconds_until_next_minute = 60 - now.time().second
        time.sleep(seconds_until_next_minute)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:  
    epd.init() 
    epd.Clear(0xFF)
    epd.sleep()
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit()
    exit()
