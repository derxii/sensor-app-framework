
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSplitter, QDockWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 
import sys
import random
from PyQt6.QtCore import QTimer, Qt
from queue import Queue
import math
import numpy as np
import re


class LiveDataPlot(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.Backend = backend
        # Set up the main window
        self.setWindowTitle("Live Data Plotting with PyQt6")
        self.setGeometry(100, 100, 800, 600)
        self.allPlots = []
        self.allMatrices = [] # List of dictionaries that include chart id, sensor and plot
        self.allHeatmaps = []
        self.allDocks = []
        self.allDockRatios = []
        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Add a button to pause/resume
        self.pause_button = QPushButton("Stop")
        self.pause_button.setFixedSize(70,70)
        layout.addWidget(self.pause_button)

        # Create all line charts from backend
        dock = None
        for chart in self.Backend.getChartObjects():
            if chart.getType() == "line":
                plot = PlotWidget()
                layout.addWidget(plot)
                self.setup_plot(plot, chart.getTitle(), chart.getxLabel(), chart.getyLabel())
                plotDict = {}
                plotDict["plot"] = plot
                plotDict["chartId"] = chart.getId()
                plotDict["counter"] = 0
                plotDict["dataStream"] = {}
                colourCount = 0
                legend = pg.LegendItem(offset=(0, -20))
                legend.setParentItem(plot.getPlotItem())
                for sensor in chart.getSensors():
                    plotDict["dataStream"][sensor] = {}
                    line = plot.plot(pen=pg.intColor(colourCount), name=sensor)
                    plotDict["dataStream"][sensor]["line"] = line
                    plotDict["dataStream"][sensor]["yData"] = []
                    plotDict["dataStream"][sensor]["xData"] = []
                    plotDict["dataStream"][sensor]["counter"] = 0
                    colourCount += 1
                    legend.addItem(line, sensor)
                legendWidth = legend.width()
                plot.getPlotItem().setContentsMargins(0, 0, legendWidth, 0) 
                self.allPlots.append(plotDict)
                dock = QDockWidget(chart.getTitle(), self)
                dock.setWidget(plot)
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
                

            if chart.getType() == "matrix":
                # Create ImageView for heatmap
                dock = QDockWidget(chart.getTitle(), self)
                widget = QWidget()
                dock.setWidget(widget)
                matrixLayout = QVBoxLayout(widget)
                imageView = pg.ImageView()
                matrixLayout.addWidget(imageView)

                #layout.addWidget(imageView)
                colormap = pg.colormap.get('turbo')  # Choose a color map
                lut = colormap.getLookupTable()  # Generate lookup table
                # Set the image with correct LUT
                image_item = imageView.getImageItem()  # Access the internal ImageItem
                image_item.setLookupTable(lut)  # Apply color map
                imageView.setColorMap(colormap)
                #(min, max) = chart.getMinMaxRange()
                #image_item.setLevels([min, max])  # Set min-max temperature range
                rangeVals = chart.getMinMaxRange()
                if rangeVals is not None:
                    (min, max) = rangeVals
                    image_item.setLevels([min, max]) 

                sensors = sorted(chart.getSensors())
                matrixDict = {"chartId":chart.getId(), "imageView": imageView, "sensors": sensors , "numSensors": len(sensors), "N": int(math.sqrt(len(sensors)))}
                self.allMatrices.append(matrixDict)
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dock)
        
                
            if chart.getType() == "heatmap":
                dock = QDockWidget(chart.getTitle(), self)
                widget = QWidget()
                dock.setWidget(widget)
                heatmapLayout = QVBoxLayout(widget)
                plot_item = pg.PlotItem()
                imageView = pg.ImageView(view=plot_item)
                heatmapLayout.addWidget(imageView)

                #layout.addWidget(imageView)
                colormap = pg.colormap.get('viridis')  # Choose a color map
                lut = colormap.getLookupTable()  # Generate lookup table
                imageView.setColorMap(colormap)
                # Set the image with correct LUT
                image_item = imageView.getImageItem()  # Access the internal ImageItem
                image_item.setLookupTable(lut)  # Apply color map
                rangeVals = chart.getMinMaxRange()
                if rangeVals is not None:
                    (min, max) = rangeVals
                    image_item.setLevels([min, max])  # Set min-max temperature range

                categories = chart.getCategories()
                #Create data struct
                
                sensors = sorted(chart.getSensors())
                # Set axis labels 
                
                plot_item.setLabel('left', chart.getyLabel())
                plot_item.setLabel('bottom', chart.getxLabel())
                x_ticks = [(i, sensors[i]) for i in range(len(sensors))]
                y_ticks = [(i, f"{categories[i][0]}-{categories[i][1]}") for i in range(len(categories))]
                plot_item.getAxis('bottom').setTicks([x_ticks])
                plot_item.getAxis('left').setTicks([y_ticks])

                dataStruct = np.zeros((len(categories), len(sensors)), dtype=float)
                heatmapDict = {"chartId":chart.getId(), "imageView": imageView, "sensors": sensors , "numSensors": len(sensors), "categories": categories, "numCategories": len(categories), "data": dataStruct}
                self.allHeatmaps.append(heatmapDict)
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dock)
                
            if dock is not None:
                self.allDocks.append(dock)
                self.allDockRatios.append(1)

        self.is_paused = False
        # Counter for x-axis
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # specifies how frequently the plot should be updated
        self.pause_button.clicked.connect(self.toggle_pause)
        self.resizeDocks(self.allDocks, self.allDockRatios, Qt.Orientation.Vertical)

    def setup_plot(self, plot_widget, title, xLabel, yLabel):
        plot_widget.setBackground('w')
        plot_widget.setTitle(title, color="k", size="16pt")
        plot_widget.setLabel("left", yLabel, color="b", size="12pt")
        plot_widget.setLabel("bottom", xLabel, color="b", size="12pt")
      
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.Backend.togglePause()
        self.pause_button.setText("Resume" if self.is_paused else "Stop")   

    def update_plot(self):
        if not self.is_paused:
            for i in range(0,len(self.allPlots)): 
                chartId = int(self.allPlots[i]["chartId"])
                for sensor in self.allPlots[i]["dataStream"].keys(): 
                    dataDict = self.Backend.getRecentChartData(chartId)
                    dataLength = dataDict[sensor].qsize()
                    plotLine = self.allPlots[i]["dataStream"][sensor]["line"]
                    for j in range(0, dataLength):
                        val = float(dataDict[sensor].get())
                        self.allPlots[i]["dataStream"][sensor]["yData"].append(val)
                        self.allPlots[i]["dataStream"][sensor]["counter"] += 1
                        self.allPlots[i]["dataStream"][sensor]["xData"].append(self.allPlots[i]["dataStream"][sensor]["counter"])

                    plotLine.setData(self.allPlots[i]["dataStream"][sensor]["xData"], self.allPlots[i]["dataStream"][sensor]["yData"])
                    self.allPlots[i]["dataStream"][sensor]["line"] = plotLine
                    
            for i in range(0,len(self.allMatrices)):
                chartId = int(self.allMatrices[i]["chartId"])
                chart = self.Backend.getChart(chartId)
                #if not chart.isQueueReady():
                #    continue
                chart = self.Backend.getChart(chartId)
                data = [] 
                for sensor in self.allMatrices[i]["sensors"]:
                    data.append(float(chart.getLastDataPoint(sensor)))
                structuredData = np.resize(np.array(data), (self.allMatrices[i]["N"], self.allMatrices[i]["N"]))
                self.allMatrices[i]["imageView"].setImage(structuredData.T)

            for i in range(0,len(self.allHeatmaps)):
                categories = self.allHeatmaps[i]["categories"]
                sensors = self.allHeatmaps[i]["sensors"]
                data = self.allHeatmaps[i]["data"]
                chartId = int(self.allHeatmaps[i]["chartId"])
                chart = self.Backend.getChart(chartId)
                for j in range(0, len(sensors)):
                    dataVal = chart.getLastDataPoint(sensors[j])
                    if dataVal is None:
                        continue
                    dataVal = float(dataVal)
                    for k in range(0, len(categories)):
                        if dataVal >= categories[k][0] and dataVal <= categories[k][1]:
                            data[k][j] += 1
                self.allHeatmaps[i]["data"] = data
                self.allHeatmaps[i]["imageView"].setImage(data.T)

    def clearPlots(self):
        for i in range(0,len(self.allPlots)): 
            for sensor in self.allPlots[i]["dataStream"].keys(): 
                self.allPlots[i]["dataStream"][sensor]["yData"] = []
                self.allPlots[i]["dataStream"][sensor]["counter"] = 0
                self.allPlots[i]["dataStream"][sensor]["xData"] = []
                plotLine = self.allPlots[i]["dataStream"][sensor]["line"]
                plotLine.setData(self.allPlots[i]["dataStream"][sensor]["xData"], self.allPlots[i]["dataStream"][sensor]["yData"])
                self.allPlots[i]["dataStream"][sensor]["line"] = plotLine
    
    def livePlotExists(self):
        return len(self.allPlots) + len(self.allMatrices) + len(self.allHeatmaps) != 0

