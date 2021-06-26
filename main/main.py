#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch14
from PIL import Image,ImageDraw,ImageFont
from gpiozero import CPUTemperature
import glob
import requests, json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch14.LCD_1inch14(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch14.LCD_1inch14()
    # Initialize library.
    disp.Init()
    disp.clear()
    while True:
        API_KEY = os.getenv("API_KEY")
        LOCATION = os.getenv("LOCATION")
        LATITUDE = os.getenv("LATITUDE")
        LONGITUDE = os.getenv("LONGITUDE")
        
        BASE_URL = 'http://api.openweathermap.org/data/2.5/onecall?'
        URL = BASE_URL + 'lat=' + LATITUDE + '&lon=' + LONGITUDE +'&appid=' + API_KEY

        response = requests.get(URL)
        data = response.json()
        current = data['current']
        currTemp = current['temp']
        feelsLike = current["feels_like"]


        daily = data['daily']
        daily_precip_float = daily[0]['pop']
        daily_temp = daily[0]['temp']
        minTemp = daily_temp['min']
        maxTemp = daily_temp['max']
        chanceOfRain = daily_precip_float * 100

        weather = current['weather']
        tempIcon = weather[0]['icon']
        
        Font0 = ImageFont.truetype("../Font/Font02.ttf",18)
        Font1 = ImageFont.truetype("../Font/Font00.ttf",35)

        image2 = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image2)

        cpu = CPUTemperature()
        temp = "CPU Temp: " + str(int(cpu.temperature)) + "C"
        draw.text((0, 0), temp, font = Font0, fill = "RED")

        feelText = "Feels Like: " + str(int(feelsLike -273.00)) + "C" 
        draw.text((0, 15), feelText, font = Font0, fill = "WHITE")

        minMax = "Min Temp: " + str(int(minTemp - 273.00)) + "C || Max Temp: " + str(int(maxTemp-273.00)) + "C"
        draw.text((0, 30), minMax, font = Font0, fill = "PURPLE")

        chanceRainText = "Chance of Rain: " + str(format(chanceOfRain, '.0f')) + "%"
        draw.text((0, 45), chanceRainText, font = Font0, fill = "BLUE")

        currTempText = str(int(currTemp - 273.00)) + "C"
        draw.text((130, 65), currTempText, font = Font1, fill = "YELLOW")
        draw.text((120, 110), datetime.today().strftime('%a %Y-%m-%d'), font = Font0, fill = "GREEN")


        picDir = "../pic/" + tempIcon + ".png"
        weatherIcon = Image.open(picDir)
        size = 65, 65
        weatherIcon.thumbnail(size)
        image2.paste(weatherIcon, (20, 70))

        disp.ShowImage(image2)
        time.sleep(100)
    disp.module_exit()
except IOError as e:
    print(e)    
except KeyboardInterrupt:
    disp.module_exit()
    exit()
