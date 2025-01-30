# Filename: Device.py
# Description: This file contains the device class and the bluetooth and serial child classes 
from bleak import BleakScanner, BleakClient
import asyncio
import re
import serial.tools.list_ports
import serial
import threading 
import time
import json 
import os 
import tempfile
class Device(object):

    def __init__(self, name, address, type):
        self.Name = name # string 
        self.Address = address # string 
        self.Sensors = set()  #[] # sensors # List of strings 
        self.ConnectedDevice = None
        self.DataBuffer = ""
        #self.DataStruct = {} # Separated into sensor data
        self.Type = type # Type is either "Bluetooth" or "Serial"
        self.Lock = threading.Lock()
        self.TerminateSession = threading.Event()
        #self.ParsedData = ""
        self.TempDataFile = tempfile.NamedTemporaryFile(suffix='.json', delete=True, delete_on_close= False)
        self.DataFilename = self.TempDataFile.name #"deviceData.json"
        self.TempRawDataFile = tempfile.NamedTemporaryFile(suffix='.json', delete=True, delete_on_close= False)
        self.RawDataFilename = self.TempRawDataFile.name#"rawData.json"

    def clearTerminateSession(self):
        self.TerminateSession.clear()

    def setTerminateSession(self):
         self.TerminateSession.set()

    def isSetTerminateSession(self):
        return self.TerminateSession.is_set()

    def addToDataBuffer(self,dataString):
        with self.Lock:
            with open(self.RawDataFilename, "r") as file:
                rawData = json.load(file)
                #dataBuffer = rawData["DataBuffer"]
            rawData["DataBuffer"] += dataString
            with open(self.RawDataFilename, "w") as file:
                json.dump(rawData, file, indent=4)
            self.DataBuffer += dataString

    def setDataBuffer(self, dataString):
        rawData = {}
        rawData["DataBuffer"] = dataString
        with self.Lock:
            self.DataBuffer = dataString
            with open(self.RawDataFilename, "w") as file:
                json.dump(rawData, file, indent=4)

    def getDataBuffer(self):
        with self.Lock:
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

    def clearDataStructValues(self):
        #for key in self.DataStruct.keys():
        #    self.DataStruct[key] = [] 
        pass

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
            #print(dataToParse)
            returnDict = {}
            dataSegments = re.split(',', dataToParse)
            items  = dataSegments[:-1]
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
              

class BluetoothDevice(Device):
    def __init__(self, name, address):
        self.characteristicUUID = ""
        self.characteristicProp = []
        self.client = None
        self.Method = "" # This indicates if the main data is received via notifications or the GATT read command
        super().__init__(name, address, "Bluetooth")


    def callback(self, sender, data):
        try:
            dataString = data.decode('utf-8')
            self.addToDataBuffer(dataString)
            #print(f"New notification: {dataString}")
        except:
            print("cannot convert notification to utf-8", flush=True)
        
    # Finds any necessary information needed about connecting to the device, finds sensor names and may create relevant client object
    async def connect(self):
        success = False 
        #iterate through all uuids and subscribe to notifications and check the data format to see if the characteristic uuid is correct
        if await BleakScanner.find_device_by_address(self.Address): 
            try:
                client = BleakClient(self.Address)
                self.client = client
                await client.connect()
                # Get the services and characteristics
                services = await client.get_services()
                for service in services:
                    for characteristic in service.characteristics:
                        self.setDataBuffer("")
                        if "notify" in characteristic.properties or "read" in characteristic.properties:
                            if "notify" in characteristic.properties: 
                                await client.start_notify(characteristic.uuid, self.callback)
                                await asyncio.sleep(1)
                                print("subscribing to notifications")
                            # Find out if the read or notify method should be used to receive data 
                            try: 
                                print(f"connection status: {client.is_connected}")
                                data = None
                                while data is None:
                                    data = await client.read_gatt_char(characteristic.uuid)                                
                                try: 
                                    notificationDataString = self.getDataBuffer()
                                    print(notificationDataString)
                                    if re.search("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", notificationDataString):
                                        self.characteristicUUID = characteristic.uuid
                                        dataString = notificationDataString
                                        self.characteristicProp = characteristic.properties
                                        print("found characteristic")
                                        success = True
                                        self.Method = "notify"
                                        print("Method is notify")
                                        # read string until 2 '\n' are found (This ensures that all sensor names are read in )
                                        while self.getDataBuffer().count('\n') < 2:
                                            await asyncio.sleep(0.05)
                                        await client.stop_notify(characteristic.uuid)
                                except:
                                    print("invalid notification string")
                                        
                                if not success:
                                    try: 
                                        readDataString = data.decode('utf-8')
                                        if re.search("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", readDataString):
                                            self.characteristicUUID = characteristic.uuid
                                            dataString = readDataString
                                            self.characteristicProp = characteristic.properties
                                            print("found characteristic")
                                            success = True
                                            self.Method = "read"
                                            print("Method is read")
                                    except:
                                        print("invalid read string")  

                                if success:
                                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", dataString)
                                    for sensorName in sensorNames:
                                        self.Sensors.add(sensorName)
                                    
                                if "notify" in characteristic.properties and not success:
                                    await client.stop_notify(characteristic.uuid)
                                    print("unsubscribing from notifications")
                                if success and client.is_connected:
                                    self.setDataBuffer("")
                                    return success
                            except: 
                                print("error occurred")            
            except:
                print("Unable to connect")
        print(f"Method: {self.Method}")
        return success
        
    async def reconnect(self):
        # This function aims to reconnect to the connected device (no information needs to be found just establish the connection again)
        if await BleakScanner.find_device_by_address(self.Address): 
            try:
                client = BleakClient(self.Address)
                self.client = client
                await self.client.connect()
                return self.client.is_connected
            except:
                print("Error: could not connect to device")
        else:
            print("Error: device address not found")
        return False

    def isConnected(self):
        return self.client.is_connected

    async def disconnect(self):
        if self.client.is_connected:
            try:
                print("disconnecting")
                await self.client.disconnect()
                print("disconnected")
                return not self.client.is_connected
            except:
                print("Error: could not disconnect")
        return False
        

    async def getData(self): 
        self.setDataBuffer("")
        #if self.Method == "notify":
        await self.client.start_notify(self.characteristicUUID, self.callback)
        while not self.TerminateSession.is_set():
            await asyncio.sleep(0.5)   
        await self.client.stop_notify(self.characteristicUUID)
        await asyncio.sleep(0.5)
        print("unsubscribing to notifications")
        '''else:
            data = None
            await self.client.start_notify(self.characteristicUUID, self.callback)
            while not self.TerminateSession.is_set():
                while data is None:
                    data = await self.client.read_gatt_char(self.characteristicUUID) 
                try:
                    dataString = data.decode("utf-8")
                    #print(dataString)
                finally:

                    #self.addToDataBuffer(dataString)
                    await asyncio.sleep(0.5)
            await self.client.stop_notify(self.characteristicUUID)'''
        

# This class if for devices that use serial port profile (SPP) 
class SerialDevice(Device):
    def __init__(self, name, address):
        super().__init__(name, address, "Serial")
    # Finds any necessary information needed about connecting to the device, finds sensor names and creates relevant client object    
    def connect(self ):
        try:
            self.serialObject = serial.Serial(self.Address, timeout=None) 
            print(self.serialObject.name)
            print(f"Serial port open: {self.serialObject.is_open}")
            if not self.serialObject.is_open:
                print("Unable to open serial port") 
            else:
                self.serialObject.reset_input_buffer()
                dataString = self.serialObject.readline()
                dataString += self.serialObject.readline()
                dataString = dataString.decode("utf-8")
                print(dataString)
                if dataString is not None and re.search("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString):  # Check that full string is read in 
                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString)
                    for sensorName in sensorNames:
                        self.Sensors.add(sensorName)
                    return True 
                self.serialObject.close()
        except:
            print("an error occurred")
        return False 
       
        
    
    # Changes data buffer if data is read in 
    # Returns true if data was successfully received and false otherwise 
    # data should be added to the objects data buffer in the form "<sensor1>: data_val, <sensor2>: data_val\n" 
    def getData(self):
        if not self.reconnect():
            self.serialObject = serial.Serial(self.Address, timeout=None) 
            print(f"Is port open: {self.serialObject.is_open}")
        self.serialObject.reset_input_buffer()
        while not self.TerminateSession.is_set():

            try:
                dataString = None 
                while dataString is None:
                    numWaitingBytes = self.serialObject.in_waiting
                    dataString = self.serialObject.read(numWaitingBytes)
                dataString = dataString.decode('utf-8')
                self.addToDataBuffer(dataString)
                modifiedString = re.sub('\s', "", dataString)
                print(modifiedString)

    
            except:
                print("an error occurred") 

    def reconnect(self):
        # This function aims to reconnect to the connected device (no information needs to be found just establish the connection again)
        if not self.serialObject.is_open:
            try:
                self.serialObject.open()
                return self.serialObject.is_open
            except:
                print("Error: could not reconnect")
        
            return False
        else:
            return True
        
    def isConnected(self):
        # returns true if connected to the device 
        return self.serialObject.is_open
    
    def disconnect(self):
        print("disconnecting...")
        if self.serialObject.is_open:
            try:
                self.serialObject.close()
                print("disconnected")
            except:
                print("Error: could not disconnect")
        return not self.serialObject.is_open
