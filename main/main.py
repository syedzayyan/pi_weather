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

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
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
