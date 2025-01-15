import numpy as np
import matplotlib.pyplot as plt

# TO DO: 
# - Complete plotChart()
class Chart(object):
    def __init__(self, chartId, chartTitle, xlabel, ylabel, sensorNames, type):
        self.Id = chartId
        self.Title = chartTitle
        self.xLabel = xlabel
        self.yLabel = ylabel
        self.SensorNames = sensorNames
        self.SensorData = {}
        self.Type = type
        
        for sensor in sensorNames:
            self.SensorData[sensor] = []

    def getData(self):
        return self.SensorData
    
    def addData(self, dataDict):
        for (sensor, dataVal) in dataDict.items():
            if sensor in self.SensorNames:
                self.SensorData[sensor].append(dataVal)

    def getLastDataPoint(self, sensorName):
        return self.SensorData[sensorName][-1] #check that no error occurs
    
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
    
    # Function for testing the backend (ignore)
    def plotChart(self):
        allDataVals = []
        xMax = 0
        for (key,val) in self.SensorData.items():
            allDataVals.append(val)
            xMax = len(val)
        plt.axis([0, xMax, min(allDataVals), max(allDataVals)])

        
