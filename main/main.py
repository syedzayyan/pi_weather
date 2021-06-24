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
        
        # Create blank image for drawing.
        URL = "http://api.openweathermap.org/data/2.5/weather?q=Ashford&appid=" + os.getenv("API_KEY")

        response = requests.get(URL)
        data = response.json()
        currTemp = data["main"]["temp"]
        feelsLike = data["main"]["feels_like"]
        minTemp = data["main"]["temp_min"]
        maxTemp = data["main"]["temp_max"]
        tempIcon = data["weather"][0]["icon"]
        
        Font0 = ImageFont.truetype("../Font/Font02.ttf",18)
        Font1 = ImageFont.truetype("../Font/Font00.ttf",35)

        image2 = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(image2)
        picDir = "../pic/" + tempIcon + ".png"
        weatherIcon = Image.open(picDir)
        size = 95, 95
        weatherIcon.thumbnail(size)
        image2.paste(weatherIcon, (15, 40))

        feelText = "Feels Like: " + str(int(feelsLike -273.00)) + "C" 
        draw.text((0, 15), feelText, font = Font0, fill = "WHITE")

        minMax = "Min Temp: " + str(int(minTemp - 273.00)) + "C || Max Temp: " + str(int(maxTemp-273.00)) + "C"
        draw.text((0, 30), minMax, font = Font0, fill = "PURPLE")


        currTempText = str(int(currTemp - 273.00)) + "C"
        draw.text((130, 50), currTempText, font = Font1, fill = "YELLOW")
        draw.text((120, 100), datetime.today().strftime('%a %Y-%m-%d'), font = Font0, fill = "BLUE")

        cpu = CPUTemperature()
        temp = "CPU Temp: " + str(cpu.temperature) + "C"
        draw.text((0, 0), temp, font = Font0, fill = "RED")
        disp.ShowImage(image2)
        time.sleep(5)    
    disp.module_exit()
except IOError as e:
    print(e)    
except KeyboardInterrupt:
    disp.module_exit()
    exit()
