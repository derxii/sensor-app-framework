# Filename: Device.py
# Description: This file contains the device class and the bluetooth and serial child classes
from bleak import BleakScanner, BleakClient
import asyncio
import re
import serial.tools.list_ports
import serial
import threading
import json 
import os 
import tempfile

class Device(object):
    def __init__(self, name, address, type):
        self.Name = name  
        self.Address = address 
        self.Sensors = set()  
        self.ConnectedDevice = None
        self.DataBuffer = ""
        self.Type = type # Type is either "Bluetooth" or "Serial"
        #self.Lock = threading.Lock()
        self.TerminateSession = threading.Event()
        self.lock = threading.Lock()
        self.pause = False
        self.TempDataFile = tempfile.NamedTemporaryFile(suffix='.json', delete=True, delete_on_close= False)
        self.DataFilename = self.TempDataFile.name
        self.TempRawDataFile = tempfile.NamedTemporaryFile(suffix='.json', delete=True, delete_on_close= False)
        self.RawDataFilename = self.TempRawDataFile.name

    def togglePause(self):
        with self.lock:
            self.pause = not self.pause

    def isPaused(self):
        with self.lock:
            val = self.pause
        return val
    
    def setPaused(self, val):
        with self.lock:
            self.pause = val
            
    def clearTerminateSession(self):
        self.TerminateSession.clear()

    def setTerminateSession(self):
        self.TerminateSession.set()

    def isSetTerminateSession(self):
        return self.TerminateSession.is_set()

    def addToDataBuffer(self, dataString):
        with self.lock:
            with open(self.RawDataFilename, "r") as file:
                rawData = json.load(file)
            rawData["DataBuffer"] += dataString
            with open(self.RawDataFilename, "w") as file:
                json.dump(rawData, file, indent=4)
            self.DataBuffer += dataString

    def setDataBuffer(self, dataString):
        rawData = {}
        rawData["DataBuffer"] = dataString
        with self.lock:
            self.DataBuffer = dataString
            with open(self.RawDataFilename, "w") as file:
                json.dump(rawData, file, indent=4)



    def getDataBuffer(self):
        with self.lock:
            dataString = self.DataBuffer
            with open(self.RawDataFilename, "r") as file:
                rawData = json.load(file)
        return rawData["DataBuffer"]

    def getDataFileName(self):
        return self.DataFilename 
    
    def formatDataStruct(self):
        deviceData = {}
        dataStruct = {}
        for sensor in self.Sensors:
            dataStruct[sensor] = []
        deviceData["DataStruct"] = dataStruct
        deviceData["ParsedData"] = ""
        
        with open(self.DataFilename, "w") as file:
            json.dump(deviceData, file, indent=4)

        with open(self.RawDataFilename, "w") as file:
            rawDataStruct = {}
            rawDataStruct["DataBuffer"] = ""
            json.dump(rawDataStruct, file, indent=4)


    def getSensorNames(self):
        return self.Sensors

    def setSensorNames(self, sensors):
        self.Sensors = sensors

    def deleteJSONFiles(self):
        if os.path.isfile(self.DataFilename):
            try:
                os.remove(self.DataFilename)
            except:
                print(f"Error: could not delete {self.DataFilename}")
        if os.path.isfile(self.RawDataFilename):
            try:
                os.remove(self.RawDataFilename)
            except:
                print(f"Error: could not delete {self.RawDataFilename}")
    
    def parseData(self):
        try:
            buffer = re.sub('\s', '', self.getDataBuffer()) 
            with open(self.DataFilename, "r") as file:
                jsonData = json.load(file)
            DataStruct = jsonData["DataStruct"] 
            jsonParsedData = jsonData["ParsedData"] 
            parsedData = re.sub('\s', '', jsonParsedData) 
            
            dataToParse = re.sub(parsedData,"", buffer)
        except:
            dataToParse = ""

        if dataToParse != "" and re.sub(",", "", dataToParse) != "":
            returnDict = {}
            dataSegments = re.split(",", dataToParse)
            items = dataSegments[:-1]
            dataToParse = ",".join(items)
            dataGroups = re.findall("<(\w+)>:([0-9\.\-]*)", dataToParse)

            
            for (sensor, dataVal) in dataGroups:
                if sensor in DataStruct.keys():
                    DataStruct[sensor].append(dataVal)
                    if sensor not in returnDict.keys():
                        returnDict[sensor] = []
                    returnDict[sensor].append(dataVal)
            jsonParsedData += dataToParse    

            deviceData = {}
            deviceData["DataStruct"] = DataStruct
            deviceData["ParsedData"] = jsonParsedData
            with open(self.DataFilename, "w") as file:
                json.dump(deviceData, file, indent=4)
            return returnDict
        return None
              


        
