#!/usr/bin/env python3
#
# Concrete display implementation using Nokia5110
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import sys
import time
import socket

#from OuterWorld import AbstractDisplay as Display

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#@Display.register
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

    def displayDemo(self):
        print('here comes the text')
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        draw.text((0,0), 'Fairytale is displaying text', font=font)
        self.disp.image(image)
        self.disp.display()
        time.sleep(1.5)

        print('now comes the cat')
        image = Image.open('/home/pi/Developer/PyPiBotter/static/images/happycat_lcd.ppm').convert('1')
        self.disp.image(image)
        self.disp.display()
        time.sleep(1.5)

        print('some shapes')
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        draw.ellipse((2,2,22,22), outline=0, fill=255)
        draw.rectangle((24,2,44,22), outline=0, fill=255)
        draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
        draw.line((68,22,81,2), fill=0)
        draw.line((68,2,81,22), fill=0)


        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        draw.text((8,30), str(ip), font=font)
        self.disp.image(image)
        self.disp.display()
        time.sleep(1.5)

        return 'drawing demo'

    def displayImage(self, imagePath):
        image = Image.open(imagePath).convert('1')

        # Alternatively load a different format image, resize it, and convert to 1 bit color.
        #image = Image.open(imagePath).resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')

        # Display image.
        self.disp.image(image)
        self.disp.display()
        return 'drawing image ' + imagePath

    def displayText(self, posX, posY, text):
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

        # Load default font.
        font = ImageFont.load_default()
        # Alternatively load a TTF font.
        # Some nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

        draw.text((posX,posY), text, font=font)
        # Display image.
        self.disp.image(image)
        self.disp.display()
        return 'drawing text ' + text + ' at position ' + str(posX) +'x'+ str(posY)


def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--demo'):
            display = Display()

            print('displaying the demo')
            status = display.displayDemo()
            print(status)

            print('finished')
        else:
            print('If you want to test the display start the script with --demo')
    else:
        print('If you want to test the display start the script with --demo')

if __name__ == '__main__':
    main()