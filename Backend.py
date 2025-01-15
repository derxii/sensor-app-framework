import asyncio
import serial.tools.list_ports
from bleak import BleakScanner, BleakClient
import re
from Device import Device, BluetoothDevice, SerialDevice
from Chart import Chart
import threading 
import csv

# TO DO: 
# -Fix the two errors outlined below
# -Save the data to the specified file location
# -Test the saveData function
# -Add data to the charts 
# -Test chart output and if they are created correctly
# -Add chart type in Chart.py
# -Add chart type getter function
# -Update backend.txt on laptop and in git repo


class Backend(object):
    def __init__(self):
        self.chartObjects = []
        self.stopSession = threading.Event()
    #connectedDevice = Device(None,None,None)
    def scanForDevices(self):
        allDevices = []
        allBluetoothDevices = asyncio.run(self.scanForBluetoothDevices())
        for device in allBluetoothDevices:
            print(f"name: {device[0]}, address: {device[1]}, rssi: {device[2]}")
            allDevices.append(device)

        allSerialDevices = self.scanForSerialDevices()
        for device in allSerialDevices:
            print(f"description: {device[0]}, port: {device[1]}")
            allDevices.append(device)

        return allDevices

    def connectToDevice(self, deviceName, deviceAddress): 
        if re.search("COM|com", deviceAddress):
            # create serial device
            self.connectedDevice = SerialDevice(deviceName, deviceAddress)
            success = self.connectedDevice.connect()
        else:
            self.connectedDevice = BluetoothDevice(deviceName, deviceAddress)
            success = asyncio.run(self.connectedDevice.connect())
        return  success #connectedDevice.connect()

    def listSensorNames(self):
        return self.connectedDevice.getSensorNames()

    def createChartObject(self, chartTitle, xlabel, ylabel, sensorNames, type):
        id = len(self.chartObjects)
        chartOb = Chart(id, chartTitle, xlabel, ylabel, sensorNames, type)
        self.chartObjects.append(chartOb)

    def getChartObjects(self):
        return self.chartObjects

    def getChart(self,id):
        return self.chartObjects[id]

    def startSession(self):
        #-Description: starts data collection session by initiating a thread process/event/subprocess with kill that changes the "inSession" variable, runs run() and another process that listens to stop the session by changing the "inSession" variable 
        #-Parameters: None
        #-Return: None
        self.connectedDevice.formatDataStruct()
        if not self.stopSession.is_set():
            #stopSession.set()
            self.stopSession.clear()
            #if connectedDevice.Type == "Bluetooth":
            #    thread = threading.Thread(target=asyncio.run, args=(runSession()), daemon=True)
            #else:
            thread = threading.Thread(target=self.runSession, daemon=True)
            thread.start()

        
        



    def runSession(self):
        #-Description: runs a while loop that continuously updates chart objects and at the end of an iteration calls a front end function to update plots
        #-Parameters: None
        #-Return: None 
        print("session started")
        while not self.stopSession.is_set():
            if self.connectedDevice.Type == "Bluetooth":
                print("bluetooth")
                asyncio.run(self.connectedDevice.getData())
                #connectedDevice.getData()
            else:
                self.connectedDevice.getData()
            print("finished receiving data")
            dataDict = self.connectedDevice.parseData()

            # Add data to charts 
            for chart in self.chartObjects:
                chart.addData(dataDict)
            print('in session\n')



    def endSession(self):
        #-Description: ends a session
        #-Parameters: None 
        #-Return: None 
        self.stopSession.set()
        print("session ended")
        if self.connectedDevice.Type == "Bluetooth":
            asyncio.run(self.connectedDevice.disconnect())

    def saveData(self, filename, filePath):
        #-Description: saves data into a csv file 
        #-Parameters: filename to save the data to <string>, filePath <string> to save the file to 
        #-Return: boolean indicating if saving the file was successful 
        success = False 
        
        data = []
        fields = list(self.connectedDevice.DataStruct.keys())
        data.append(fields)
        numRows = len(self.connectedDevice.DataStruct[fields[0]])    
        for i in range(0, numRows):
            currentRow = []
            for field in fields:
                currentRow.append(self.connectedDevice.DataStruct[field][i])
            data.append(currentRow)

        # Save to a specific file location
        # Check if the directory exists
        # Create the directory if it does not exst by using os.makedirs()
        # Append filename to filepath 
        # Add .csv to the end of the file name 
        filename = filename + ".csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(data)

        
            
                
            


        # Save the file into the specifies file location

    def restartSession(self):
        #-Description: start a new session by clearing the current data in the chart 
        #-Parameters: None
        #-Return: None 
        pass

    def restartProgram(self):
        #-Description: clears all charts and disconnects PC from bluetooth device 
        #-Parameters: None
        #-Return: None 
        pass
        
        

    ########################### Helper functions ###############################
    # Helper for scanForDevices()    
    async def scanForBluetoothDevices(self):
        availableDevices = []
        devices = await BleakScanner.discover()
        for d in devices:
            name = d.name
            if name is None:
                name = "unknown"
            availableDevices.append((name, d.address, d.rssi))
        return availableDevices


    # Helper for ScanForDevices 
    def scanForSerialDevices(self):
        availablePorts = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            #availablePorts.append((port.name, port.device))
            availablePorts.append((port.name, port.device))
        return availablePorts

    def printAllData(self):
        for (key, value) in self.connectedDevice.DataStruct.items():
            print(f"{key}: {value}")

        for chart in self.chartObjects:
            print(f"Chart id: {chart.getId()}")
            print(f"Title: {chart.getTitle()}")
            print(f"x label: {chart.getxLabel()}")
            print(f"y label: {chart.getyLabel()}")
            print(f"Type : {chart.getType()}")
            for (key, value) in chart.getData().items():
                print(f"{key}: {value}")

    ############################################## TESTING CODE ########################################################


    async def scanAndConnectBluetoothDevices():
        availableDevices = []
        devices = await BleakScanner.discover()
        for d in devices:
            name = d.name
            if name is None:
                name = "unknown"
            availableDevices.append((name, d.address, d.rssi))
            print(f"Name: {name}, Address: {d.address}")
            if name == "Esther's A33":
                deviceOb = BluetoothDevice(name, d.address)
                await deviceOb.connect()
                print("finished connecting")
                deviceOb.formatDataStruct()
                print("finished formatting data")
                
                for i in range(0, 40):
                    await deviceOb.getData()
                    print("finished receiving data")
                    deviceOb.parseData()
                for (key, value) in deviceOb.DataStruct.items():
                    print(f"{key}: {value}")

    '''
    async def main():
        availableDevices = []
        devices = await BleakScanner.discover()
        for d in devices:
            name = d.name
            if name is None:
                name = "unknown"
            availableDevices.append((name, d.address, d.rssi))
            print(f"Name: {name}, Address: {d.address}")
            if name == "Esther's A33":
                deviceOb = BluetoothDevice(name, d.address)
                await deviceOb.connect()
                print("finished connecting")
                deviceOb.formatDataStruct()
                print("finished formatting data")
                userInput = input()
                if userInput == "1":
                    startSession()
                if userInput == "2":
                    endSession()
                    

                userInput = input()
                if userInput == "1":
                    startSession()
                if userInput == "2":
                    endSession()
                restartProgram()

                restartProgram()
    '''


def main():
    backend = Backend()
    allDevices = backend.scanForDevices()
    deviceName = input("Enter the name of the device you want to connect to: ")
    deviceAddress = input("Enter the address of the device you want to connect to: ")
    returnVal = backend.connectToDevice(deviceName, deviceAddress)
    print(f"Success: {returnVal}")
    if not returnVal:
        return
    print("Found the following sensors:")
    for sensor in backend.listSensorNames():
        print(sensor)
    

    numCharts = int(input("How many charts do you want?: "))
    print(numCharts)

    for _ in range(0, numCharts):
        chartTitle = input("Enter the chart title: ")
        xlabel = input("Enter x label: ")
        ylabel = input("Enter y label: ")
        sensorNameStr = input("Enter the sensors you want to use (enter in the format: sensor1 sensor2): ")
        sensorNames = re.split(' ', sensorNameStr)
        chartType = input("Enter the chart type: ")
        print(sensorNames)

        backend.createChartObject(chartTitle, xlabel, ylabel, sensorNames, chartType)
    userInput = input("Press 1 to start session: ")
    if userInput == "1":
        backend.startSession()

    userInput = input("Press 2 to end session: ")

    if userInput == "2":
        backend.endSession()
    backend.printAllData()

    userInput = input("Would you like to save the data to a csv file? (y/n): ")
    if userInput == "y":
        filename = input("What would you like to save the filename as?: ")
        fileLocation = input("where would you like to save the file?: ")
        backend.saveData(filename, fileLocation)
            


if __name__ == "__main__":
    #allBluetoothDevices = asyncio.run(scanAndConnectBluetoothDevices())
    
    '''
    allSerialDevices = scanForSerialDevices()
    for device in allSerialDevices:
        print(f"Name: {device[0]}, port: {device[1]}")
        if device[1] == "COM9":
            print(connectToDevice(device[0], device[1]))
    '''
   # asyncio.run(main())
    main()
    
