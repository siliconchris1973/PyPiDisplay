import os
import json

class RfidTag():
    # represents one RFID Tag
    __ID = ""
    __tagID = ""
    __Characters = 0

    __Checksum = 0
    __Checksum_Tag = 0
    __Tag = 0

    # Flags
    __Startflag = "\x02"
    __Endflag = "\x03"

    __rfidTagData = {}
    __rfidAllTagsData = {}
    __rfidAllTagsJsonData = {}

    __storagePath = "/home/pi/rfidTagData/"
    __jsonFileExtension = "json"
    __rfidJsonDataFile = ""

    def __init__(self):
        pass

    def setTagData(self, rfidTag):
        self.ID = rfidTag

        # Checksumme berechnen
        for I in range(0, 9, 2):
            self.Checksum ^= ((int(self.ID[I], 16)) << 4) + int(self.ID[I + 1], 16)
        self.Checksum = hex(self.Checksum)

        # Tag herausfiltern
        self.Tag = ((int(self.ID[1], 16)) << 8) + ((int(self.ID[2], 16)) << 4) + ((int(self.ID[3], 16)) << 0)
        self.Tag = hex(self.Tag)
        self.tagID = self.ID[4:10]

        self.rfidTagData['TagId'] = self.tagID
        self.rfidTagData['Tag'] = self.Tag
        self.rfidTagData['Checksum'] = self.Checksum
        self.rfidTagData['Rawdata'] = self.ID

        self.rfidJsonData = json.dumps(self.rfidTagData)

        # define the storage path and file for this tag
        self.rfidJsonDataFile = self.storagePath + self.tagID + "." + self.jsonFileExtension

    def getTagAsJson(self):
        return self.rfidJsonData

    def storeTag(self):
        try:
            with open(self.rfidJsonDataFile, 'w') as outfile:
                json.dump(outfile, self.rfidTagData)
                outfile.close()
        except IOError:
            print("ERROR :: filesystem is read only, could not store RFID Tag data")
        except:
            print("ERROR :: unknown error while storing RFID Tag.data")

    def retrieveTag(self):
        try:
            with open(self.rfidJsonDataFile, 'r') as infile:
                json.load(infile, self.rfidJsonData)
        except IOError:
            print("ERROR :: IOError while retrieving RFID Tag data")
        except:
            print("ERROR :: unknown error while retrieving RFID Tag.data")

    def isTagStored(self):
        if (os.path.isfile(self.rfidJsonDataFile)):
            return True
        else:
            return False
