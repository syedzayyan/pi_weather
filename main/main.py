#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch14
from PIL import Image,ImageDraw,ImageFont
from gpiozero import CPUTemperature
import glob
import requests, json

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

URL = "http://api.openweathermap.org/data/2.5/weather?q=London&appid=" + os.environ["API_KEY"]

# Pre-load icons into a dictionary with PIL
icons = {}

for icon in glob.glob("../pic/*.png"):
    icon_name = icon.split("/")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image

response = requests.get(URL)
data = response.json()
print(data)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch14.LCD_1inch14(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch14.LCD_1inch14()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    # Create blank image for drawing.
    
    Font0 = ImageFont.truetype("../Font/Font00.ttf",20)
    
    image2 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image2)

    image2.paste(icons["01d"], (10, 46))

    cpu = CPUTemperature()
    temp = "CPU Temp: " + str(cpu.temperature)
    logging.info("draw text")
    draw.text((0, 45), temp, font = Font0, fill = "BLACK")
    disp.ShowImage(image2)
    time.sleep(5)

    
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
