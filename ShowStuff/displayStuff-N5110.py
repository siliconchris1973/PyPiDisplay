#!/usr/bin/env python
#
# little script to display hostname, kernel and ip address of a Raspberry Pi on a Nokia5110 LCD
# 
# author:  pibotter@gmx.de
# version: 0.1.0
# date:    6th August 2016
# 
# based on Adafruit LCD library and example Adafruit scripts
# 

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import sys
import time
import socket
import platform

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

appDebug = True

class Display():
    # Raspberry Pi hardware SPI config:
    DC_PORT = 23
    RST_PORT = 24
    SPI_PORT = 0
    SPI_DEVICE = 0
     
    CONTRAST = 60
    MAX_SPEED_HZ = 4000000

    disp = object
    image = object
    draw = object
    customFont='./fairytale.ttf' # currently must be in same directory as script
    font = object

    def __init__(self):
        if appDebug:
            print('initializing display class')
        # Initialize library.
        self.disp = LCD.PCD8544(self.DC_PORT, self.RST_PORT, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=self.MAX_SPEED_HZ))
        self.disp.begin(contrast=self.CONTRAST)
        self.image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

        try:
            #self.font = ImageFont.load_path(self.customFont)
            #self.font = ImageFont.truetype(font=self.customFont, size=10, index=0, encoding='')
            self.font = ImageFont.truetype("arial.ttf", 12)
        except IOError:
            if appDebug:
                print('ttf font not loaded, falling back to default font')
            self.font = ImageFont.load_default()

        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

        # Clear display.
        self.disp.clear()
        self.disp.display()
        if appDebug:
            print('display class initialized')

    def getNetworkIp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
        except:
            if appDebug:
                print('no network detected')
            return 'no network'
        else:
            if appDebug:
                print('network detected ' + str(s.getsockname()[0]))
            return str(s.getsockname()[0])

    def showSysInfo(self):
        if appDebug:
            print('showSysInfo called')
        system = platform.uname()[0]
        hostname = platform.uname()[1]
        kernel = platform.uname()[2]
        arch = platform.uname()[4]

        self.draw.text((10,0), hostname, font=self.font)
        self.draw.line((0,11,96,11), fill=0)
        self.draw.text((0,12), system + ' ' + kernel, font=self.font)
        self.draw.text((0,20), arch, font=self.font)
        self.draw.text((0,36), self.getNetworkIp(), font=self.font)
        self.disp.image(self.image)
        self.disp.display()

def main():
    if (len(sys.argv) > 1):
        display = Display()

        if (sys.argv[1] == '--sysinfo'):
            if appDebug:
                print('command line argument --sysinfo')
            display.showSysInfo()
        else:
            print('Currently only system information is output by this script. Call it with --sysinfo')
    else:
        print('Currently only system information is output by this script. Call it with --sysinfo')

if __name__ == '__main__':
    main()
