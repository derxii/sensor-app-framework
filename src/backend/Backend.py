# Filename: Backend.py
# Description: This file contains the backend functions that should be accessed by the frontend
import asyncio
import serial.tools.list_ports
from bleak import BleakScanner
import re
from Device import BluetoothDevice, SerialDevice
from Chart import Chart
from LiveDataPlot import LiveDataPlot
from StaticDataPlot import StaticDataPlot
import threading 
import csv
import os 
import json

# Plotting libraries 
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
import sys
import qasync

# TO DO: 
# - when a heatmap is created the error doesn't pop up
# - stop data collection and plotting before ending the session
# - get rid of the pause button when session ends 
# - add to requirements.txt
# - create functions that clear the central widgetd
# - Test file directory checking on a macbook
# - Deal with serial connection issue when sensor names aren't received

# NOTE
# Data should be sent to the program in the following format: <sensor1>: dataval, <sensor2>: dataval, <sensor3>: dataval, \n
# Also note that the last comma is needed 

class Backend(object):
    def __init__(self):
        self.figures = []
        self.chartObjects = []
        self.stopSession = threading.Event()
        
    async def scanForDevices(self):
        allDevices = []
        allBluetoothDevices = await self.scanForBluetoothDevices()
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
            success = await self.connectedDevice.connect() 
        return  success 
    
    def togglePause(self):
        self.connectedDevice.togglePause()

    def listSensorNames(self):
        return self.connectedDevice.getSensorNames()

    def createChartObject(self, chartTitle, xlabel, ylabel, sensorNames, type):
        if len(self.chartObjects) >= 1:
            id = self.chartObjects[-1].getId() + 1
        else:
            id = 0
        if len(self.chartObjects) >= 1:
            id = self.chartObjects[-1].getId() + 1
        else:
            id = 0
        chartOb = Chart(id, chartTitle, xlabel, ylabel, sensorNames, type)
        self.chartObjects.append(chartOb)
        return id

    def deleteChart(self, id):
        deleted_idx = -1
        for idx, chart in enumerate(self.chartObjects):
            if chart.getId() == id:
                deleted_idx = idx

        self.chartObjects.pop(deleted_idx)
        
    def getChartObjects(self):
        return self.chartObjects

    def getChart(self,id):
        for chart in self.chartObjects:
            if chart.getId() == id:
                return chart
        return None

    
    def getChartInfo(self, id):
        chart = self.getChart(id)
        chartInfo = {}
        chartInfo["id"] = chart.getId()
        chartInfo["Title"] = chart.getTitle()
        chartInfo["xLabel"] = chart.getxLabel()
        chartInfo["yLabel"] = chart.getyLabel()
        chartInfo["Type"] = chart.getType()
        chartInfo["Sensors"] = chart.getSensors()
    
    def getAllChartData(self, id):
        return self.getChart(id).getAllData()
    
    def getRecentChartData(self, id):
        return self.getChart(id).getRecentData()
        
    def runInLoop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connectedDevice.getData())

    def runSessionInLoop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.runSession())

    async def startSession(self):
        self.connectedDevice.formatDataStruct()
        if not self.connectedDevice.isSetTerminateSession():
            self.connectedDevice.clearTerminateSession()
            self.stopSession.clear()
            '''if self.connectedDevice.Type == "Bluetooth":
                print("Attempting to create thread")
                loop = asyncio.new_event_loop()
                self.getDataThread = threading.Thread(target=self.runInLoop, args=(loop,), daemon=True)
            else:
                self.getDataThread = threading.Thread(
                    target=self.connectedDevice.getData, daemon=True
                )

            self.getDataThread.start()
            self.runSessionThread = threading.Thread(
                target=self.runSession, daemon=True
            )
            self.runSessionThread.start()'''
            
            #self.runSessionThread = threading.Thread(target=self.runSession, daemon=True)
            #self.runSessionThread.start()
            '''if self.connectedDevice.Type == "Bluetooth":
                print("Attempting to create thread")
                loop = asyncio.new_event_loop()
                self.runSessionThread= threading.Thread(target=self.runSessionInLoop, args=(loop,), daemon=True)
            else:
                self.runSessionThread= threading.Thread(
                    target=self.runSession, daemon=True
                )'''
            #self.runSession()
            #loop = asyncio.new_event_loop()
            #self.runSessionThread= threading.Thread(target=self.runSessionInLoop, args=(loop,), daemon=True)
            #self.runSessionThread.start()
            self.runSessionThread = threading.Thread(target=self.runSession, daemon=True)
            self.runSessionThread.start()

    def runSession(self):
        while not self.stopSession.is_set():
            if self.connectedDevice.Type == "Serial":
                self.connectedDevice.getData()
            dataDict = self.connectedDevice.parseData()
            if dataDict is None:
                continue
            for chart in self.chartObjects:
                chart.addData(dataDict)
           
    async def endSession(self):
        self.connectedDevice.setPaused(True)
        self.connectedDevice.setTerminateSession()
        self.stopSession.set()
        #self.getDataThread.join()
        self.runSessionThread.join()
        print("session ended")
        self.connectedDevice.clearTerminateSession()
        self.stopSession.clear()


    def saveData(self, filePath):
        # Check if the directory exists
        directory = None
        if re.search(r'\\', filePath):
            splitPath = re.split(r'\\', filePath)
            directories = splitPath[:-1]
            directory = r'\\'.join(directories)
        elif re.search("/", filePath): # Directory format for windows   
            splitPath = re.split("/", filePath)
            directories = splitPath[:-1]
            directory = "/".join(directories)
        if directory is not None and not os.path.isdir(directory): # Directory format for MAC
            print("Error: directory not found")
            return False
        # Check if the filepath already exists 
        print(filePath)
        if os.path.exists(filePath):
            print("Error: file already exists in the specified directory")
            return False 
        dataFilename = self.connectedDevice.getDataFileName()
        with open(dataFilename, "r") as file:
            deviceData = json.load(file)
        DataStruct = deviceData["DataStruct"]
        fileNameComponents = re.split( r"\.", filePath)
        exten = fileNameComponents[1]

        # determine whether the file is a .txt or .csv 
        if exten == "csv":
            data = []
            fields = list(DataStruct.keys())
            data.append(fields) # first row of the csv include the fields 
            
            allRowLengths = [len(DataStruct[sensor]) for sensor in fields]
            maxNumRows = max(allRowLengths) 
            for i in range(0, maxNumRows):
                currentRow = []
                for field in fields:
                    if i < len(DataStruct[field]):
                        currentRow.append(DataStruct[field][i])
                    else:
                        currentRow.append("")
                data.append(currentRow)
            try:
                with open(filePath, 'w', newline='', encoding='utf-8') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerows(data)
            except:
                print("Error: unable to create csv file")
                return False
            return True  
        
        elif exten == "txt":
            with open(filePath, "w", encoding="utf-8") as file:
                for (key, value) in DataStruct.items():
                    print(f"{key}: [", end="", file=file)
                    for i in range(len(value)):
                        print(value[i], end="", file=file)
                        if i != len(value) - 1:
                            print(", ", end="", file=file)
                    print("]", file=file)
                
    def clearSession(self):
        self.connectedDevice.setPaused(False) 
        self.connectedDevice.setDataBuffer("")
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
        self.connectedDevice.setPaused(False)
        if self.connectedDevice.Type == "Bluetooth":       
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
        self.chartObjects = []

        
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
            availablePorts.append((port.name, port.device, float("inf")))
        return availablePorts

    def printAllData(self):
        for chart in self.chartObjects:
            print(f"Chart id: {chart.getId()}")
            print(f"Title: {chart.getTitle()}")
            print(f"x label: {chart.getxLabel()}")
            print(f"y label: {chart.getyLabel()}")
            print(f"Type : {chart.getType()}")
            for key, value in chart.getData().items():
                print(f"{key}: {value}")


   
    ############################################## TESTING CODE ########################################################

def main():
    backend = Backend()
    app = QApplication(sys.argv)     
    loop = qasync.QEventLoop(app)    
    asyncio.set_event_loop(loop)
    count = 0
    while True:
        userInput = input(
            "Would you like to start the program from the beginning (1) restart a data recording session (2) or exit the program (3)?: "
        )
        if userInput == "3":
            #backend.restartProgram()
            loop.run_until_complete(backend.restartProgram())
            break
        elif userInput == "1":
            if count != 0:
                #backend.restartProgram()
                loop.run_until_complete(backend.restartProgram())
            loop.run_until_complete(backend.scanForDevices())
            deviceName = input("Enter the name of the device you want to connect to: ")
            deviceAddress = input("Enter the address of the device you want to connect to: ")
            #backend.connectToDevice(deviceName, deviceAddress)
            returnVal = loop.run_until_complete(backend.connectToDevice(deviceName, deviceAddress))
            print(f"Connection success: {returnVal}")
            if not returnVal:
                return
            print("Found the following sensors:")
            for sensor in backend.listSensorNames():
                print(sensor)
            numCharts = int(input("How many charts do you want?: "))
            for _ in range(0, numCharts):
                print("#################################################### CREATING NEW CHART ###############################################################")
                chartType = input("Enter the chart type: ")
                chartTitle = input("Enter the chart title: ")
                xlabel = ""
                ylabel = ""
                if chartType == "line" or chartType == "heatmap":
                    xlabel = input("Enter x label: ")
                if chartType != "pie":
                    ylabel = input("Enter y label: ")
                sensorNameStr = input("Enter the sensors you want to use (enter in the format: sensor1 sensor2): ")
                sensorNames = re.split(' ', sensorNameStr)
                print(f"The following sensors were chosen: {sensorNames}") 
                chartId = backend.createChartObject(chartTitle, xlabel, ylabel, sensorNames, chartType)
                chart = backend.getChart(chartId)
                if chartType == "pie":
                    rangesString = input("Enter the value ranges for the chart categories (enter in the format: low1-high1 low2-high2): ") #note that if no range is given then the chart will use each data value as a category
                    ranges = re.findall("([0-9\.\-]*)\-([0-9\.\-]*)", rangesString)
                    rangeList = []
                    print("Range:", end=" ") 
                    for (low, high) in ranges:
                        rangeList.append((float(low),float(high)))
                        print(f"({float(low)},{float(high)})", end=" ")
                    print()
                    chart.setCategories(rangeList)
                if chartType == "heatmap":
                    rangeString = input("Enter the min-max range for sensor data values (enter in the format: min-max): ")
                    if rangeString != "":
                        minMax = re.findall("([0-9\.\-]*)\-([0-9\.\-]*)", rangeString)
                        chart.setMinMaxRange((float(minMax[0][0]), float(minMax[0][1])))
                    rangesString = input("Enter the value ranges for the chart categories (enter in the format: low1-high1 low2-high2): ") #note that if no range is given then the chart will use each data value as a category
                    ranges = re.findall("([0-9\.\-]*)\-([0-9\.\-]*)", rangesString)
                    rangeList = []
                    print("Range:", end=" ") 
                    for (low, high) in ranges:
                        rangeList.append((float(low),float(high)))
                        print(f"({float(low)},{float(high)})", end=" ")
                    print()
                    chart.setCategories(rangeList)
                if chartType == "matrix":
                    rangeString = input("Enter the min-max range for sensor data values (enter in the format: min-max): ")
                    if rangeString != "":
                        minMax = re.findall("([0-9\.\-]*)\-([0-9\.\-]*)", rangeString)
                        chart.setMinMaxRange((float(minMax[0][0]), float(minMax[0][1])))
                    
        elif userInput == "2":
            print("Automatically restarting session")
            backend.clearSession()
       
        userInput = input("Press enter to start session: ")
        backend.clearSession()
        if backend.connectedDevice.Type == "Bluetooth":
            loop.run_until_complete(backend.connectedDevice.startNotifications())
        loop.run_until_complete(backend.startSession())
        
        window = QMainWindow()
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)
        LiveWindow = LiveDataPlot(backend, window, layout)

        if LiveWindow.livePlotExists():
            window.show()
            app.processEvents()
            
        
        userInput = input("Press enter to end session: ")
        loop.run_until_complete(backend.endSession())
        if backend.connectedDevice.Type == "Bluetooth":
            loop.run_until_complete(backend.connectedDevice.stopNotifications())
        LiveWindow.set_pause(True)
    
        StaticWindow = StaticDataPlot(backend, window)
        if StaticWindow.staticPlotExists():
            window.show()
            app.processEvents()
    
        userInput = input("Would you like to save the data to a csv/txt file? (y/n): ")
        if userInput == "y":
            fileLocation = input("where would you like to save the file?: ")
            backend.saveData(fileLocation)
        count += 1

if __name__ == "__main__":
    main()