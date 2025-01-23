# Filename: Backend.py
# Description: This file contains the backend functions that should be accessed by the frontend
import asyncio
import serial.tools.list_ports
from bleak import BleakScanner, BleakClient
import re
from Device import Device, BluetoothDevice, SerialDevice
from Chart import Chart
import threading 
import csv
import os 
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Plotting libraries 
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import random
from PyQt6.QtCore import QTimer
from queue import Queue
# TO DO: 
# -Add timestamp for data where t=0 is when the data was received 
# -deal with frontend timeout
# -Simulate chart plotting 
# -Update backend.txt on laptop and in git repo
# -Fix issue where read method is checked for when conditions for notify method are satisfied
# -Re implement Chart.getData()
# -Complete getChartData()
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

    def listSensorNames(self):
        return self.connectedDevice.getSensorNames()

    def createChartObject(self, chartTitle, xlabel, ylabel, sensorNames, type):
        id = len(self.chartObjects)
        chartOb = Chart(id, chartTitle, xlabel, ylabel, sensorNames, type)
        self.chartObjects.append(chartOb)

        #figureTuple = self.createFigure()
        #self.figures.append(figureTuple)

    # The following code is to simulate plotting 
    

    def getChartObjects(self):
        return self.chartObjects

    def getChart(self,id):
        return self.chartObjects[id]
    
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
        for chart in self.chartObjects:
                chart.plotChart()

    def saveData(self, filename, filePath):
        #-Description: saves data into a csv file in the specified location
        #-Parameters: filename to save the data to <string>, filePath <string> to save the file to 
        #-Return: boolean indicating if saving the file was successful 
        if not os.path.isdir(filePath):
            print("Error: directory not found")
            return False
        #check if the full filepath already exists 
        fullPath = filePath + filename + ".csv"
        print(fullPath)
        if os.path.exists(fullPath):
            print("Error: file already exists in the specified directory")
            return False 
        dataFilename = self.connectedDevice.getDataFileName()
        with open(dataFilename, "r") as file:
            deviceData = json.load(file)
        DataStruct = deviceData["DataStruct"]

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
            

    def clearSession(self):
        #-Description: start a new session by clearing the current data in the chart 
        #-Parameters: None
        #-Return: None 
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
class LiveDataPlot(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.Backend = backend
        # Set up the main window
        self.setWindowTitle("Live Data Plotting with PyQt6")
        self.setGeometry(100, 100, 800, 600)

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Create a pyqtgraph PlotWidget
        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget)

        # Set up the plot
        self.plot_widget.setBackground('w')  # Set background to white
        self.plot_widget.setTitle("Live Data Plot", color="b", size="20pt")
        self.plot_widget.setLabel("left", "Value", color="r", size="14pt")
        self.plot_widget.setLabel("bottom", "Time", color="r", size="14pt")
        self.plot_widget.addLegend()

        # Add a plot line
        self.plot_line = self.plot_widget.plot(pen=pg.mkPen(color='b', width=2), name="Random Data")

        # Initialize data
        self.x_data = []
        self.y_data = []

        # Set up a QTimer for live updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update every 100 ms

        # Counter for x-axis
        self.counter = 0

    def update_plot(self):
        """Updates the plot with new random data."""
        #self.counter += 1
        #self.x_data.append(self.counter)  # Increment x-axis data
        #chart = self.Backend.getChart(0)
        dataDict = self.Backend.getRecentChartData(0)#chart.getRecentData()
        
        data = []
        for key in dataDict.keys():
            data = dataDict[key]
            print(key)
            
        #self.x_data.append(len(data))
        dataSize = data.qsize()
        #self.x_data.append(dataSize)
        #print(data)
        for i in range(dataSize):
           val = float(data.get())
           self.y_data.append(val) 
           self.counter += 1
           self.x_data.append(self.counter)
           #print(f"{val} ", end="")
           #print("")
        #chartData = []

        #for val in data:
        #    self.y_data.append(float(val))
        #if len(data) != 0:
            #self.y_data.append(chartData)  # Add random y-axis data

            # Limit the data to keep the plot from growing indefinitely
        #self.x_data = self.x_data[-100:]  # Keep only the last 100 points
        #self.y_data = self.y_data[-100:]

            # Update the plot
        self.plot_line.setData(self.x_data, self.y_data)

# Main shows the order and usage of backend functions
async def main():
    backend = Backend()         
    count = 0
    while True:
        userInput = input("Would you like to start the program from the beginning (1) restart a data recording session (2) or exit the program (3)?: ")
        if userInput == "3":
            await backend.restartProgram()
            break
        elif userInput == "1":
            if count != 0:
                await backend.restartProgram()
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

        elif userInput == "2":
            print("Automatically restarting session")
            backend.clearSession()
            
        userInput = input("Press 1 to start session: ")
        if userInput == "1":
            backend.clearSession()
            await backend.startSession()

        # Comment out the following lines of code to run the program like normal
        app = QApplication(sys.argv)
        main_window = LiveDataPlot(backend)
        main_window.show()
        sys.exit(app.exec())
        # End of comment section

        userInput = input("Press 2 to end session: ")
        if userInput == "2":    
            await backend.endSession()
        
    
        userInput = input("Would you like to save the data to a csv file? (y/n): ")
        if userInput == "y":
            filename = input("What would you like to save the filename as?: ")
            fileLocation = input("where would you like to save the file?: ")
            backend.saveData(filename, fileLocation)
        count += 1


if __name__ == "__main__":
    asyncio.run(main())
    
