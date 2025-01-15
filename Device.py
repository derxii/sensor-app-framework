# Filename: Device.py
# Description: This file contains the device class and the bluetooth and serial child classes 
from bleak import BleakScanner, BleakClient
import asyncio
import re
import serial.tools.list_ports
import serial

'''
def callback(sender, data):
        #stringData = data.decode('utf-8')
        print(f"recieved: {data} from {sender}")
        return data
'''


class Device(object):

    def __init__(self, name, address, type):
        self.Name = name # string 
        self.Address = address # string 
        self.Sensors = set()  #[] # sensors # List of strings 
        self.ConnectedDevice = None
        self.DataBuffer = ""
        self.DataStruct = {} # Separated into sensor data
        self.Type = type # Type is either "Bluetooth" or "Serial"

    def formatDataStruct(self):
        for sensor in self.Sensors:
            self.DataStruct[sensor] = []

    def getSensorNames(self):
        return self.Sensors
        
    def setSensorNames(self, sensors):
        self.Sensors = sensors

    def parseData(self):
        # strip white spaces 
        # create capture groups for sensor names and then data values 
        # Add data values into dictionary and return the parsed data as a dictionary
        print('Parsing data')
        dataString = re.sub('\s', '', self.DataBuffer)
        dataGroups = re.findall("<(\w+)>:([0-9\.\-]*)", dataString)
        returnDict = {}
        for (sensor, dataVal) in dataGroups:
            if sensor in self.DataStruct.keys():
                self.DataStruct[sensor].append(dataVal)
                returnDict[sensor] = dataVal
        return returnDict

class BluetoothDevice(Device):
    def __init__(self, name, address):
        self.characteristicUUID = ""
        self.characteristicProp = []
        self.client = None
        self.NotificationBuffer = ""
        self.Method = "" # This indicates if the main data is received via notifications or the GATT read command
        super().__init__(name, address, "Bluetooth")


    def callback(self, sender, data):
        #stringData = data.decode('utf-8')
        print(f"recieved: {data} from {sender}")
        try:

            self.NotificationBuffer += data.decode('utf-8')
        except:
            print("cannot convert notification to utf-8")
        return data
    
    # Finds any necessary information needed about connecting to the device, finds sensor names and may create relevant client object
    async def connect(self):
        success = False 
        #iterate through all uuids and subscribe to notifications and check the data format to see if the characteristic uuid is correct
        if await BleakScanner.find_device_by_address(self.Address): #and await BleakScanner.find_device_by_address(self.Name): #note that the MAC address may change so find another way to connect to device 
            try:
                #async with BleakClient(self.Address) as client:
                client = BleakClient(self.Address)
                self.client = client
                await client.connect()
                # Get the services and characteristics
                services = await client.get_services()

                for service in services:
                    print(f"Service UUID: {service.uuid}")
                    for characteristic in service.characteristics:
                        print(f"  Characteristic UUID: {characteristic.uuid}")
                        print(f"characteristic UUID properties: {characteristic.properties}")
                        if "notify" in characteristic.properties or "read" in characteristic.properties: #and re.search("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", client.read_gatt_char(characteristic.uuid)):
                            if "notify" in characteristic.properties: 
                                await client.start_notify(characteristic.uuid, self.callback)
                                print("subscribing to notifications")
                            # Find out if the read or notify method should be used to receive data 
                            try: 
                                print(f"connection status: {client.is_connected}")
                                data = None
                                while data is None:
                                    data = await client.read_gatt_char(characteristic.uuid)
                                #print(f"data: {data}")
                                #data = await client.start_notify(characteristic.uuid, self.callback)
                                print(f"notification data: {self.NotificationBuffer}")
                                print(f"Read data: {data}")
                                
                                try: 
                                    notificationDataString = self.NotificationBuffer #.decode('utf-8')
                                    print(notificationDataString)
                                    if re.search("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", notificationDataString):
                                        self.characteristicUUID = characteristic.uuid
                                        dataString = notificationDataString
                                        self.characteristicProp = characteristic.properties
                                        print("found characteristic")
                                        success = True
                                        self.Method = "notify"
                                        await client.stop_notify(characteristic.uuid)
                                except:
                                    print("invalid notification string")    
                                if not success:
                                    # try read data 
                                    
                                    try: 
                                        readDataString = data.decode('utf-8')
                                        if re.search("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", readDataString):
                                            self.characteristicUUID = characteristic.uuid
                                            dataString = readDataString
                                            self.characteristicProp = characteristic.properties
                                            print("found characteristic")
                                            success = True
                                            self.Method = "read"
                                    
                                    except:
                                        print("invalid read string")  

                                if success:
                                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", dataString)
                                    for sensorName in sensorNames:
                                        self.Sensors.add(sensorName)
                                '''
                                if dataString is not None and re.search("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", dataString): # ensure the data string is not empty
                                    correctFormat = True
                                    self.characteristicUUID = characteristic.uuid
                                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.\-]*\s*,?\s*", dataString)
                                    for sensorName in sensorNames:
                                        self.Sensors.add(sensorName)
                                    #self.Sensors = sensorNames
                                    self.characteristicProp = characteristic.properties
                                    print("found characteristic")
                                    success = True
                                '''    
                                
                                    
                                if "notify" in characteristic.properties and not success:
                                    await client.stop_notify(characteristic.uuid)
                                    print("unsubscribing from notifications")
                                if success and client.is_connected:
                                    #await client.disconnect()
                                    return success
                            except: 
                                print("error occurred")
                if client.is_connected:
                    await client.disconnect()              
            except:
                print("Unable to connect")
        
        return success
        
    # Changes data buffer if data is read in 
    # Returns true if data was successfully received and false otherwise 
    # data should be added to the objects data buffer in the form "<sensor1>: data_val, <sensor2>: data_val\n" 
    async def disconnect(self):
        await self.client.stop_notify(self.characteristicUUID)
        await self.client.disconnect()
        print("unsubscribing from notifications")



    async def getData(self):
        success = False 
        print(self.Method)
        # Note that when the method is "notify" the program does not get past the following line
        #if await BleakScanner.find_device_by_address(self.Address): #and await BleakScanner.find_device_by_address(self.Name): #note that the MAC address may change so find another way to connect to device 
            #print("found address")
        try:
            if self.Method == "notify": 
                #Clear previous notifications 
                self.NotificationBuffer = ""
                print("starting notifications")
                await self.client.start_notify(self.characteristicUUID, self.callback)
                print("Receiving notifications")
                    #asyncio.sleep(0.5)
                await self.client.stop_notify(self.characteristicUUID)
                print(self.NotificationBuffer)
                if  re.search("\s*<\w+>:\s*[0-9\.\-]*\s*,?\s*", self.NotificationBuffer):
                    self.DataBuffer = self.NotificationBuffer
                    success = True
                        
            else:
                data = None
                while data is None:
                    data = await self.client.read_gatt_char(self.characteristicUUID) # Check that full string is read in 
                dataString = data.decode("utf-8")
                print(dataString)
                if  re.search("\s*<\w+>:\s*[0-9\.\-]*\s*,?\s*", dataString):
                    self.DataBuffer = dataString
                    success = True    
        except:
            print("unable to connect to device")
                
        return success
    #def findCharacteristicUUID(self.address):
        
       

class SerialDevice(Device):
    # for devices that use serial port profile (SPP)
    def __init__(self, name, address):
        super().__init__(name, address, "Serial")
    # Finds any necessary information needed about connecting to the device, finds sensor names and may create relevant client object    
    def connect(self ):
        
        try:
            self.serialObject = serial.Serial(self.Address) #serial.Serial(self.Address, 9600, timeout=10, parity=serial.PARITY_NONE)
            print(self.serialObject.name)
            #self.serialObject.open()
            print(f"Serial port open: {self.serialObject.is_open}")
            if not self.serialObject.is_open:
                print("Unable to open serial port") 
            else:
                # Note that TextIOWrapper may be needed 
                
                dataString = self.serialObject.readline()
                #while dataString is None:
                #    dataString = self.serialObject.readline()
                dataString += self.serialObject.readline()
                dataString = dataString.decode("utf-8")
                print(dataString)
    
                if dataString is not None and re.search("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString):  # Check that full string is read in 
                    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString)
                    #print(f"sensor names: {sensorNames}")
                    #self.Sensors = sensorNames 
                    for sensorName in sensorNames:
                        self.Sensors.add(sensorName)
                    #self.serialObject.close()
                    return True 
                self.serialObject.close()
        except:
            print("an error occurred")
        return False 
       
        
    
    # Changes data buffer if data is read in 
    # Returns true if data was successfully received and false otherwise 
    # data should be added to the objects data buffer in the form "<sensor1>: data_val, <sensor2>: data_val\n" 
    def getData(self):
        try:
            #self.serialObject = serial.serial(self.Address, 9600, timeout=10, parity=serial.PARITY_NONE)
            #self.serialObject.open()
            if not self.serialObject.is_open:
                print("Unable to open serial port") 
            else:
            # Note that TextIOWrapper may be needed 
            
                dataString = self.serialObject.readline()
                
                dataString = dataString.decode('utf-8')
                print(dataString)
                if dataString is not None and re.search("\s*<\w+>:\s*[0-9\.\-]*\s*,?\s*", dataString):  # Check that full string is read in 
                    #sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString)  
                    self.DataBuffer = dataString
                    #self.serialObject.close()
                    return True 
                #self.serialObject.close()
        except:
            print("an error occurred")
        return False 
            
            







############################################################## TESTING CODE ###########################################################################


async def scanForBluetoothDevices():
    availableDevices = []
    devices = await BleakScanner.discover()
    for d in devices:
        name = d.name
        if name is None:
            name = "unknown"
        availableDevices.append((name, d.address, d.rssi))
        deviceOb = BluetoothDevice(name, d.address)
        print(f"Name: {name}, Address: {d.address}")
        await deviceOb.connect()
        
        
    return availableDevices

def parseDataTesting(DataStruct, dataString):
    # strip white spaces 
    # create capture groups for sensor names and then data values 
    # Add data values into dictionary
    print('Parsing data')
    dataString = re.sub('\s', '', dataString)
    print(dataString)
    dataGroups = re.findall("<(\w+)>:([0-9\.\-]*)", dataString)
    for (sensor, dataVal) in dataGroups:
        if sensor in DataStruct.keys():
            DataStruct[sensor].append(dataVal)
        

if __name__ == "__main__":
    dataDict = {} 
    dataString1 = "<sensor1>: 3920.22, <sensor2>: 483.22, <sensor3>: 3343\n"
    sensorNames = re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", dataString1)
    for sensor in sensorNames:
        dataDict[sensor] = []

    dataString2 = "<sensor1>: 1212.1212, <sensor2>: 33939.22, <sensor3>: 33049947.22\n <sensor1>: 224548.2235"
    parseDataTesting(dataDict, dataString2)
    for key in dataDict.keys():
        print(f"{key}: {dataDict[key]}")

#allBluetoothDevices = asyncio.run(scanForBluetoothDevices())
#for device in allBluetoothDevices:
#    print(f"name: {device[0]}, address: {device[1]}, rssi: {device[2]}")
    #allDevices.append(device)

'''
print(re.search("\s*<\w+>:\s*[0-9\.]+\s*,?", "<sensor1>: 1.2"))
print(re.search("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", "<sensor1>: 12"))
print(re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", "<sensor1>: 1.2, <sensor2>: 3.2, <sp20> "))
print(re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", "<sensor1>: 1.2, <sensor2>: 3.2, <sp20>: 13"))
'''
#print(re.findall("\s*<(\w+)>:\s*[0-9\.]*\s*,?\s*", "<sensor1>: 1.2, <sensor2>: 3.2, <sp20>: 13\n"))
#print(re.search("\s*<\w+>:\s*[0-9\.]*\s*,?\s*", "<sensor1>: 1.2, <sensor2>: 3.2, <sp20>: 13\n"))


