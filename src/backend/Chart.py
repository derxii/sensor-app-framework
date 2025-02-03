# Filename: Chart.py
# Description: This file contains the Chart class 
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import json
import threading
from queue import Queue
import re
# TO DO: 
# - change getData()
# - Change the chart class so that it only stores recent data and stores the rest of the data in a json file
class Chart(object):
    def __init__(self, chartId, chartTitle, xlabel, ylabel, sensorNames, type):
        self.Id = chartId
        self.Title = chartTitle
        self.xLabel = xlabel
        self.yLabel = ylabel
        self.SensorNames = sensorNames
        self.chartLock = threading.Lock()
        #self.SensorData = {}
        self.CurrentSensorData = {}
        self.Type = type
        self.TempChartFile = tempfile.NamedTemporaryFile(suffix='.json', delete=True, delete_on_close= False) # This file contains all the chart data 
        self.ChartFilename = self.TempChartFile.name 
        self.MinMaxRange = None

        SensorData = {}   
        for sensor in sensorNames:
            SensorData[sensor] = []
        with open(self.ChartFilename, "w") as file:
            json.dump(SensorData, file, indent=4)
        for sensor in sensorNames:
            self.CurrentSensorData[sensor] = Queue()  #[] #[]

    # returns data received since the last time getCurrentData was called. This function should be used when plotting live data 
    def getRecentData(self):
        #with self.chartLock:
        returnData = self.CurrentSensorData
        #for sensor in self.CurrentSensorData.keys():
            #self.CurrentSensorData[sensor] = []
        return returnData

    def getAllData(self):
        with open(self.ChartFilename, "r") as file:
            SensorData = json.load(file)
        return SensorData
    
    def addData(self, dataDict):
        with open(self.ChartFilename, "r") as file:
            SensorData = json.load(file)
        for (sensor, dataVal) in dataDict.items():
            if sensor in self.SensorNames:
                #with self.chartLock:
                for val in dataVal:
                    SensorData[sensor].append(val)
                    #self.SensorData[sensor].append(val)
                    #self.CurrentSensorData[sensor].append(val)
                    if re.sub("\s", "", val) != "":
                        self.CurrentSensorData[sensor].put(val)
        with open(self.ChartFilename, "w") as file:
            json.dump(SensorData, file, indent=4)

    def getLastDataPoint(self, sensorName):
        #with open(self.ChartFilename, "r") as file:
        #    SensorData = json.load(file)
        #return SensorData[sensorName][-1] #check that no error occurs
        return self.CurrentSensorData[sensorName].get()
    
    def getId(self):
        return self.Id 
    
    def getTitle(self):
        return self.Title
    
    def getxLabel(self):
        return self.xLabel
    
    def getyLabel(self):
        return self.yLabel
    
    def getType(self):
        return self.Type
    
    def getSensors(self):
        return self.SensorNames
    # Function for testing the backend (ignore for frontend)
    def plotChart(self):
        with open(self.ChartFilename, "r") as file:
            SensorData = json.load(file)
        plt.title(self.Title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        format = 'g.'
        if self.Type == 'line':
            format = 'b-'
        for (key,val) in SensorData.items():
            xAxis = np.arange(0, len(val))
            plt.plot(xAxis, val, label=key)
        plt.show()

    def clearData(self):
        with open(self.ChartFilename, "r") as file:
            SensorData = json.load(file)

        for key in SensorData.keys():
            SensorData[key] = []

        with open(self.ChartFilename, "w") as file:
            json.dump(SensorData, file, indent=4)
        
    def setCategories(self, allCategories):
        self.AllCategories = allCategories # list of tuples 

    def getCategories(self):
        return self.AllCategories
    
    def setMinMaxRange(self, range):
        self.MinMaxRange = range # tuple

    def getMinMaxRange(self):
        return self.MinMaxRange

    def isQueueReady(self):
        for sensor in self.SensorNames:
            if self.CurrentSensorData[sensor].empty():
                return False
        return True
        
