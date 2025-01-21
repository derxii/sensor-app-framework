import asyncio
import serial.tools.list_ports
from bleak import BleakScanner, BleakClient
import re
from Device import Device, BluetoothDevice, SerialDevice
from Chart import Chart
import threading 
import csv
import os 

# TO DO: 
# -Implement restartSession
# -Implement restartProgram
# -Test restartSession
# -Test restartProgram
# -Fix the two errors outlined in backend.txt
# -Update backend.txt on laptop and in git repo
# -Test the case where the MAC address of the bluetooth device changes 
# -Fix issue where read method is checked for when conditions for notify method are satisfied
# -Check that device is subscribing to notifications correctly
# -Check if read method needs device to subscribe to notification (check ble documentation)

class Backend(object):
    def __init__(self):
        self.chartObjects = []
        self.stopSession = threading.Event()
    async def scanForDevices(self):
        allDevices = []
        allBluetoothDevices = await self.scanForBluetoothDevices() #asyncio.run(self.scanForBluetoothDevices())
        for device in allBluetoothDevices:
            print(f"name: {device[0]}, address: {device[1]}, rssi: {device[2]}")
            allDevices.append(device)

        allSerialDevices = self.scanForSerialDevices()
        for device in allSerialDevices:
            print(f"Name: {device[0]}, port: {device[1]}")
            allDevices.append(device)

        return allDevices

    async def connectToDevice(self, deviceName, deviceAddress): 
        if re.search("COM|com", deviceAddress):
            self.connectedDevice = SerialDevice(deviceName, deviceAddress)
            success = self.connectedDevice.connect()
        else:
            self.connectedDevice = BluetoothDevice(deviceName, deviceAddress)
            success = await self.connectedDevice.connect() #asyncio.run(self.connectedDevice.connect())
        return  success 

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
    
    '''
    def getChartData(self,id):
        sensorNames = self.getChart(id).SensorNames
        chartData = {}
        for sensor in sensorNames:
            chartData[sensor] = self.connectedDevice.DataStruct[sensor]
        return chartData
    '''
    
    def runInLoop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connectedDevice.getData())

    def runSessionInLoop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.runSession())

    async def startSession(self):
        #-Description: starts data collection session by initiating a thread processes and initialising kill variable 
        #-Parameters: None
        #-Return: None
        self.connectedDevice.formatDataStruct()
        if not self.connectedDevice.isSetTerminateSession():
            self.connectedDevice.clearTerminateSession()
            self.stopSession.clear()
            if self.connectedDevice.Type == "Bluetooth":
                #if self.connectedDevice.Method == "read":
                print("Attempting to create thread")
                loop = asyncio.new_event_loop()
                self.getDataThread = threading.Thread(target=self.runInLoop, args=(loop,), daemon=True) # threading.Thread(target=asyncio.run, args=(self.connectedDevice.getData(),), daemon=True) #
                #self.getDataThread.start()
                #self.runSessionThread = threading.Thread(target=self.runSession, daemon=True)
                #else:
                #    loop = asyncio.new_event_loop()
                #    self.runSessionThread = threading.Thread(target=self.runSessionInLoop, args=(loop,), daemon=True)
                #self.runSessionThread.start()
                #else:
                #    await self.connectedDevice.client.start_notify(self.connectedDevice.characteristicUUID, self.connectedDevice.callback)

            else:
                self.getDataThread = threading.Thread(target=self.connectedDevice.getData, daemon=True)
            
            self.getDataThread.start()
            self.runSessionThread = threading.Thread(target=self.runSession, daemon=True)
            self.runSessionThread.start()

    def runSession(self):
        #-Description: runs a while loop that continuously updates chart objects and at the end of an iteration calls a front end function to update plots
        #-Parameters: None
        #-Return: None 
        print("session started")
        
        while not self.stopSession.is_set():
            dataDict = self.connectedDevice.parseData()
            if dataDict is None:
                continue
            # Add data to charts 
            for chart in self.chartObjects:
                chart.addData(dataDict)
                
            



    async def endSession(self):
        #-Description: ends a session
        #-Parameters: None 
        #-Return: None 
        
        #if self.connectedDevice.Type == "Bluetooth": 
        #    await self.connectedDevice.disconnect()
    
        self.connectedDevice.setTerminateSession()
        self.stopSession.set()
        self.getDataThread.join()
        
        self.runSessionThread.join()


        
        print("session ended")
        self.connectedDevice.clearTerminateSession()
        self.stopSession.clear()
        #if self.connectedDevice.Type == "Bluetooth":
        #    asyncio.run(self.connectedDevice.disconnect())
        for chart in self.chartObjects:
                chart.plotChart()

    def saveData(self, filename, filePath):
        #-Description: saves data into a csv file in the specified location
        #-Parameters: filename to save the data to <string>, filePath <string> to save the file to 
        #-Return: boolean indicating if saving the file was successful 

        if not os.path.isdir(filePath):
            #os.makedirs(filePath)
            print("Error: directory not found")
            return False

        #check if the full filepath already exists 
        fullPath = filePath + filename + ".csv"
        print(fullPath)
        if os.path.exists(fullPath):
            print("Error: file already exists in the specified directory")
            return False 

        data = []
        fields = list(self.connectedDevice.DataStruct.keys())
        data.append(fields) # first row of the csv include the fields 
        allRowLengths = [len(self.connectedDevice.DataStruct[sensor]) for sensor in fields]
        maxNumRows = max(allRowLengths) 
        for i in range(0, maxNumRows):
            currentRow = []
            for field in fields:
                if i < len(self.connectedDevice.DataStruct[field]):
                    currentRow.append(self.connectedDevice.DataStruct[field][i])
                else:
                    currentRow.append("")
            data.append(currentRow)
        try:
            with open(fullPath, 'w', newline='', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerows(data)
        except:
            print("Error: unable to create csv file")
            return False

        return True  
            

    def clearSession(self):
        #-Description: start a new session by clearing the current data in the chart 
        #-Parameters: None
        #-Return: None 
        self.connectedDevice.clearDataStructValues()
        for chart in self.chartObjects:
            chart.clearData()
        # Confirm connection and attempt to reconnect maximum 5 times if not connected
        reconnectCount = 0
        reconnectSuccess = self.connectedDevice.isConnected()
        while not reconnectSuccess and reconnectCount < 5:
            reconnectSuccess = self.connectedDevice.reconnect()
            reconnectCount += 1
        if not reconnectSuccess:
            print("Error: failed to reconnect")
            return 
     


    async def restartProgram(self):
        #-Description: clears all charts and disconnects PC from bluetooth device 
        #-Parameters: None
        #-Return: None
        if self.connectedDevice.Type == "Bluetooth":
            #asyncio.run(self.connectedDevice.disconnect())
            #await self.connectedDevice.disconnect()
            
            if self.connectedDevice.client.is_connected:
                try:
                    print("disconnecting")
                    await self.connectedDevice.client.disconnect()
                    print("disconnected")
                    return not self.connectedDevice.client.is_connected
                except:
                    print("Error: could not disconnect")
            return False
            
        else:
            self.connectedDevice.disconnect()
        
        
        

    ########################### Backend class helper functions ###############################
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


async def main():
    backend = Backend()
    allDevices = await backend.scanForDevices()
    deviceName = input("Enter the name of the device you want to connect to: ")
    deviceAddress = input("Enter the address of the device you want to connect to: ")
    returnVal = await backend.connectToDevice(deviceName, deviceAddress)
    print(f"Success: {returnVal}")
    if not returnVal:
        return
    print("Found the following sensors:")
    for sensor in backend.listSensorNames():
        print(sensor)
    

    numCharts = int(input("How many charts do you want?: "))
    for _ in range(0, numCharts):
        chartTitle = input("Enter the chart title: ")
        xlabel = input("Enter x label: ")
        ylabel = input("Enter y label: ")
        sensorNameStr = input("Enter the sensors you want to use (enter in the format: sensor1 sensor2): ")
        sensorNames = re.split(' ', sensorNameStr)
        print(f"The following sensors were chosen: {sensorNames}")
        chartType = input("Enter the chart type: ")
        backend.createChartObject(chartTitle, xlabel, ylabel, sensorNames, chartType)
    userInput = input("Press 1 to start session: ")
    if userInput == "1":
        await backend.startSession()

    userInput = input("Press 2 to end session: ")

    if userInput == "2":
        await backend.endSession()
    #backend.printAllData()

    userInput = input("Would you like to save the data to a csv file? (y/n): ")
    if userInput == "y":
        filename = input("What would you like to save the filename as?: ")
        fileLocation = input("where would you like to save the file?: ")
        backend.saveData(filename, fileLocation)
            
    
    while True:
        userInput = input("Would you like to restart the session (1) or exit the program (2)?: ")
        if userInput == "1":
            print("Automatically restarting session")
            userInput = input("Press 1 to start session: ")
            if userInput == "1":
                backend.clearSession()
                backend.startSession()
            userInput = input("Press 2 to end session: ")

            if userInput == "2":
                backend.endSession()
        if userInput == "2":
            #backend.restartProgram()
           # asyncio.run(backend.restartProgram())
            await backend.restartProgram()
            break


if __name__ == "__main__":
    asyncio.run(main())
    
