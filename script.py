#!/usr/bin/env python3
import sys
import time
from os import path

import logging
from logging.handlers import RotatingFileHandler


# to change the display implementation you only need to change the import here.
#from ShowStuff import Nokia5110 as Display
from ShowStuff import DummyDisplay as Display
from util import RFIDReader as RFIDreader
from util import simpleLogin as userSession

_cwd = path.dirname(path.abspath(__file__))

display = Display.Display()
rfid = RFIDreader.RFIDReader()

def main():
    handler = RotatingFileHandler('/var/tmp/PyPiDisplay.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)

    appDebug=False

    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--server'):
            pass
        elif (sys.argv[1] == '--debug'):
            appDebug = True
        else:
            print('running all in console mode - please use --server to start a background server')
    else:
        print('running all in console mode and with debugging on - please use --server to start a background server')
        appDebug = True

    if appDebug:
        print("starting up")

    while True:
        lasttag = ""
        tag = rfid.run()
        if tag != lasttag:
            if appDebug:
                print("displaying new tag")
            display.displayText(0, 30, tag)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
