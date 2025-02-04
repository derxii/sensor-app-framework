# Filename: Backend.py
# Description: This file contains the backend functions that should be accessed by the frontend
import asyncio
import serial.tools.list_ports
from bleak import BleakScanner, BleakClient
import re
from Device import Device, BluetoothDevice, SerialDevice
from Chart import Chart
from LiveDataPlot import LiveDataPlot
from StaticDataPlot import StaticDataPlot
import threading 
import csv
import os 
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Plotting libraries 
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSplitter, QDockWidget, QLabel
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import random
from PyQt6.QtCore import QTimer, Qt, QEventLoop
from queue import Queue
import qasync
# TO DO: 
#  Resize docks
# -Add timestamp for data where t=0 is when the data was received 
# -deal with frontend timeout
# -Update backend.txt on laptop and in git repo
# -Fix issue where read method is checked for when conditions for notify method are satisfied
# data should be sent to the program in the following format: <sensor1>: dataval, <sensor2>: dataval, <sensor3>: dataval, \n
# note that the last comma is needed 

class Backend(object):
    def __init__(self):
        self.figures = []
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
    
    def togglePause(self):
        self.connectedDevice.togglePause()


    
    def listSensorNames(self):
        return self.connectedDevice.getSensorNames()

    def createChartObject(self, chartTitle, xlabel, ylabel, sensorNames, type):
        if len(self.chartObjects) >= 1:
            id = self.chartObjects[-1].getId() + 1
        else:
            id = 0
        chartOb = Chart(id, chartTitle, xlabel, ylabel, sensorNames, type)
        self.chartObjects.append(chartOb)
        return id

        #figureTuple = self.createFigure()
        #self.figures.append(figureTuple)

    # The following code is to simulate plotting 
    

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
                self.getDataThread = threading.Thread(target=self.runInLoop, args=(loop,), daemon=True)
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
        self.connectedDevice.setTerminateSession()
        self.stopSession.set()
        self.getDataThread.join()
        self.runSessionThread.join()
        print("session ended")
        self.connectedDevice.clearTerminateSession()
        self.stopSession.clear()
        #for chart in self.chartObjects:
        #        chart.plotChart()

    def saveData(self, filename, filePath):
        #-Description: saves data into a csv file in the specified location
        #-Parameters: filename to save the data to <string>, filePath <string> to save the file to 
        #-Return: boolean indicating if saving the file was successful 

        # determine whether the file is a .txt or .csv 
        
        if not os.path.isdir(filePath):
            print("Error: directory not found")
            return False
        #check if the full filepath already exists 
        
        fullPath = filePath + filename  #+ ".csv"
        print(fullPath)
        if os.path.exists(fullPath):
            print("Error: file already exists in the specified directory")
            return False 
        dataFilename = self.connectedDevice.getDataFileName()
        with open(dataFilename, "r") as file:
            deviceData = json.load(file)
        DataStruct = deviceData["DataStruct"]

        fileNameComponents = re.split( r"\.", filename)
        exten = fileNameComponents[1]

        if exten == "csv":
            data = []
            fields = list(DataStruct.keys())
            data.append(fields) # first row of the csv include the fields 
            
            #allRowLengths = [len(self.connectedDevice.DataStruct[sensor]) for sensor in fields]
            allRowLengths = [len(DataStruct[sensor]) for sensor in fields]
            maxNumRows = max(allRowLengths) 
            for i in range(0, maxNumRows):
                currentRow = []
                for field in fields:
                    #if i < len(self.connectedDevice.DataStruct[field]):
                    #    currentRow.append(self.connectedDevice.DataStruct[field][i])
                    if i < len(DataStruct[field]):
                        currentRow.append(DataStruct[field][i])
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
        
        elif exten == "txt":
            with open(fullPath, "w", encoding="utf-8") as file:
                for (key, value) in DataStruct.items():
                    print(f"{key}: [", end="", file=file)
                    for i in range(len(value)):
                        print(value[i], end="", file=file)
                        if i != len(value) - 1:
                            print(", ", end="", file=file)
                    print("]", file=file)
                
                    
            

    def clearSession(self):
        #-Description: start a new session by clearing the current data in the chart 
        #-Parameters: None
        #-Return: None
        self.connectedDevice.setPaused(False) 
        self.connectedDevice.clearDataStructValues()
        self.connectedDevice.setDataBuffer("")
        #self.connectedDevice.ParsedData = ""
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
            availablePorts.append((port.name, port.device))
        return availablePorts

    def printAllData(self):
        #for (key, value) in self.connectedDevice.DataStruct.items():
        #    print(f"{key}: {value}")

        for chart in self.chartObjects:
            print(f"Chart id: {chart.getId()}")
            print(f"Title: {chart.getTitle()}")
            print(f"x label: {chart.getxLabel()}")
            print(f"y label: {chart.getyLabel()}")
            print(f"Type : {chart.getType()}")
            for (key, value) in chart.getData().items():
                print(f"{key}: {value}")

def updateChart(frame):
    pass

    ############################################## TESTING CODE ########################################################

def main():
    backend = Backend()
    app = QApplication(sys.argv)     
    loop = qasync.QEventLoop(app)    
    asyncio.set_event_loop(loop)
    count = 0
    while True:
        userInput = input("Would you like to start the program from the beginning (1) restart a data recording session (2) or exit the program (3)?: ")
        if userInput == "3":
            #await backend.restartProgram()
            loop.run_until_complete(backend.restartProgram())
            break
        elif userInput == "1":
            if count != 0:
                #await backend.restartProgram()
                loop.run_until_complete(backend.restartProgram())
            #allDevices = await backend.scanForDevices()
         
            loop.run_until_complete(backend.scanForDevices())
            #app.exec()
            deviceName = input("Enter the name of the device you want to connect to: ")
            deviceAddress = input("Enter the address of the device you want to connect to: ")
            loop.run_until_complete(backend.connectToDevice(deviceName, deviceAddress))
            #print(f"Success: {returnVal}")
            #if not returnVal:
            #    return
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
                    #minMax = re.findall("([0-9\.\-]*)\-([0-9\.\-]*)", rangeString)
                    #chart.setMinMaxRange((float(minMax[0][0]), float(minMax[0][1])))
                    

        elif userInput == "2":
            print("Automatically restarting session")
            backend.clearSession()
            #LiveWindow.clearPlots()

            
        userInput = input("Press enter to start session: ")
        backend.clearSession()
        #await backend.startSession()
        loop.run_until_complete(backend.startSession())
        
        LiveWindow = LiveDataPlot(backend)
        if LiveWindow.livePlotExists():
            LiveWindow.show()
            app.processEvents()
        
        userInput = input("Press enter to end session: ")
        loop.run_until_complete(backend.endSession())

        StaticWindow = StaticDataPlot(backend)
        if StaticWindow.staticPlotExists():
            StaticWindow.show()
    
        userInput = input("Would you like to save the data to a csv/txt file? (y/n): ")
        if userInput == "y":
            filename = input("What would you like to save the filename as?: ")
            fileLocation = input("where would you like to save the file?: ")
            backend.saveData(filename, fileLocation)
        count += 1


if __name__ == "__main__":
    #asyncio.run(main())
    main()
    
