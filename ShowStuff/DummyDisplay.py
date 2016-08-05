#!/usr/bin/env python3
#
# the dummy display implementation simply returning some text
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#

import sys
#from OuterWorld import AbstractDisplay as Display

#@Display.register
class Display():

    def __init__(self):
        pass

    def displayImage(self, imagePath):
        return 'drawing image ' + str(imagePath)

    def displayText(self, posX, posY, text):
        return 'drawing text ' + text + ' at position ' + str(posX) +'x'+ str(posY)

def main():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '--demo'):
            display = Display()
            status = display.displayText(0,0,'demo')
            print(status)
        else:
            print('If you want to test the display start the script with --demo')
    else:
        print('Usually this script should not be run standalone. \n'
              'If you want to test the display start the script with --demo')

if __name__ == '__main__':
    main()