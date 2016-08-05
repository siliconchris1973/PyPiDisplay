#!/usr/bin/env python3
#
# Abstract display definition
#
# Author:   pibotter@gmx.de
# Version:  0.0.1
# Date:     1st Aug. 2016
#

import sys
import abc

class Display(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError( "Should have implemented this" )

    @abc.abstractmethod
    def displayImage(self,imagePath):
        raise NotImplementedError( "Should have implemented this" )

    @abc.abstractmethod
    def displayText(self, posX, posY, text):
        raise NotImplementedError( "Should have implemented this" )


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