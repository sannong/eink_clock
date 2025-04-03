#!/usr/bin/python
# -*- coding:utf-8 -*-
# Initially copied from https://pastebin.com/VwYQcFD3 and reddit thread and modified
# https://www.reddit.com/r/raspberry_pi/comments/vi2xow/i_made_a_basic_clock_with_a_pi_zero_and_an_eink/?utm_source=share&utm_medium=web2x&context=3

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
print(libdir)
print(picdir)     

import logging
from waveshare_epd import epd2in13_V4
import time
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

epd = epd2in13_V4.EPD()

try:
    font76 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 76)   
    font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)    
    font52 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 52)
    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    print(epd.height)
    print(epd.width)
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
        
    while (True):
          
        if (start_hour != datetime.now().hour):
            start_hour = datetime.now().hour
            epd.init()
            epd.Clear(0xFF)
            epd.displayPartBaseImage(epd.getbuffer(time_image2))
            
        time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)
        time_draw.text((125, 55), datetime.now().strftime('%H:%M'), font = font76, fill = 0, anchor="mm")
        time_draw.text((125, 122), datetime.now().strftime('%a, %d %B'), font = font30, fill = 0, anchor="md")
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
