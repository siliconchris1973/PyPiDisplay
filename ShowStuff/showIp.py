#!/usr/bin/env python
#
# Concrete display implementation using Nokia5110
#
#

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import sys
import time
import socket

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display():
    # Raspberry Pi hardware SPI config:
    DC_PORT = 23
    RST_PORT = 24
    SPI_PORT = 0
    SPI_DEVICE = 0
     
    CONTRAST = 60
    MAX_SPEED_HZ = 4000000
    # Hardware SPI usage:
    disp = LCD.PCD8544(DC_PORT, RST_PORT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=MAX_SPEED_HZ))
     
    def __init__(self):
        # Initialize library.
        self.disp.begin(contrast=self.CONTRAST)
         
        # Clear display.
        self.disp.clear()
        self.disp.display()
    def getIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip

    def showIp(self):
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
         
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
         
        draw.text((0,0), 'My IP on wlan0 is:', font=font)
        draw.text((0,30), str(ip), font=font)
        self.disp.image(image)
        self.disp.display()

def main():
    display = Display()
    display.showIp()

if __name__ == '__main__':
    main()
