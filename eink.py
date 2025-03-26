#!/usr/bin/python
# -*- coding:utf-8 -*-
# copied from https://pastebin.com/VwYQcFD3 and reddit thread 
# https://www.reddit.com/r/raspberry_pi/comments/vi2xow/i_made_a_basic_clock_with_a_pi_zero_and_an_eink/?utm_source=share&utm_medium=web2x&context=3
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
print(libdir)    
import logging
from waveshare_epd import epd2in13_V4
import time
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

epd = epd2in13_V4.EPD()

try:    
    font52 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 52)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    
    # partial update
    logging.info("4.show time...")
        
    while (True):
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)
        time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255)
        time_draw.text((125, 61), datetime.now().strftime('%H:%M'), font = font52, fill = 0, anchor="mm")
        time_draw.text((125, 122), datetime.now().strftime('%a, %d %B %Y'), font = font24, fill = 0, anchor="md")
        epd.display(epd.getbuffer(time_image.transpose(Image.ROTATE_180)))
        
        if (datetime.now().hour == 0):
            seconds_until_next_630 = (datetime.timedelta(hours=24) - (now - now.replace(hour=6, minute=30, second=0, microsecond=0))).total_seconds() % (24 * 3600)
            epd.Clear(0xFF)
            epd.sleep()
            time.sleep(seconds_until_next_630)
            epd.init(epd.FULL_UPDATE)
            epd.Clear(0xFF)
            continue
        
        now = datetime.now()
        seconds_until_next_minute = 60 - now.time().second
        time.sleep(seconds_until_next_minute)

        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:   
    epd.Clear(0xFF) 
    epd.sleep()
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
