#!/usr/bin/env python3
#
# little script to read RFID Tags from a RDM6300 and store them in some DB instance (currently file)
#
# author:  pibotter@gmx.de
# version: 0.1.0
# date:    12th August 2016
#
# based on http://chris-labs.de/electronics/raspberrypi/2015/02/19/raspberrypi-rdm6300-rfid-reader.html
#

import serial
import time
import sys

try:
    from util.RFIDTag import RfidTag as RfidTag
except ImportError:
    from RFIDTag import RfidTag as RfidTag

appDebug = False

class RFIDReader():
    serialInterfaceDevice = "/dev/ttyAMA0"
    serialInterfaceDeviceBaud = 9600

    ID = ""

    # Flags
    Startflag = "\x02"
    Endflag = "\x03"

    rfidTag = object
    rfidTagData = {}
    rfidJsonData = {}
    rfidAllTagsData = {}
    rfidAllTagsJsonData = {}
    allReadTags = []
    rfidTagNumber = 0

    storagePath = "/home/pi/rfidTagData/"
    jsonFileExtension = "json"
    rfidJsonDataFile = ""

    try:
        UART = serial.Serial(serialInterfaceDevice, serialInterfaceDeviceBaud)
    except FileNotFoundError:
        print("ERROR :: could not open serial device")
    except Exception:
        print("ERROR :: could not open serial device")


    def __init__(self):
        # UART oeffnen
        try:
            self.UART.close()
            self.UART.open()
        except FileNotFoundError:
            print("ERROR :: could not open serial device")
        except Exception:
            print("ERROR :: could not open serial device")

        self.rfidTagNumber = 0

    def run(self):
        self.read()
        newRfidTag = RfidTag(self.rfidTag)

        # now check that we did not scan this tag already in this current run
        # and also, that even in case we did scan it, the file still exists
        # if we did not scan the tag in this run or if the file does not exit,
        # although we scanned the tag, we need to go on and scan and store it
        if (newRfidTag.tagID in self.allReadTags and newRfidTag.isTagStored()):
            pass
        else:
            if appDebug:
                print("New Tag " + newRfidTag.tagID + " found")

            self.allReadTags.append(newRfidTag.tagID)

            if (newRfidTag.isTagStored()):
                if appDebug:
                    print("Tag " + newRfidTag.tagID + " already stored")
            else:
                if appDebug:
                    # Ausgabe der Daten
                    print("")
                    print("New Tag " + newRfidTag.tagID)
                    print("------------------------------------------")
                    print("Datensatz: ", newRfidTag.ID)
                    print("Tag: ", newRfidTag.Tag)
                    print("ID: ", newRfidTag.tagID)
                    print("Checksumme: ", newRfidTag.Checksumme)
                    print("------------------------------------------")

                newRfidTag.storeTag()
                if appDebug:
                    print("Waiting for next Tag")
                    print("")

    def stop(self):
        self.UART.close()

    def read(self):
        # Zeichen einlesen
        Zeichen = self.UART.read()

        # Uebertragungsstart signalisiert worden?
        if Zeichen == self.Startflag:
            # ID zusammen setzen
            for Counter in range(13):
                Zeichen = self.UART.read()
                self.rfidTag = self.rfidTag + str(Zeichen)

            # Endflag aus dem String loeschen
            self.rfidTag = self.rfidTag.replace(self.Endflag, "" )
            return self.rfidTag


def main():
    if (len(sys.argv) > 1):
        readTags = RFIDReader()

        if (sys.argv[1] == '--readtags'):
            appDebug = True
            if appDebug:
                print("Starting up - press Ctrl + C to stop")
            try:
                while True:
                    readTags.run()
                    time.sleep(0.5)
            except KeyboardInterrupt:
                print("closing ...")
                readTags.stop()

        else:
            print("If called from command line, you can only read RFID tags with this script. Call it with --readtags")
    else:
        print("If called from command line, you can only read RFID tags with this script. Call it with --readtags")

if __name__ == '__main__':
    main()
