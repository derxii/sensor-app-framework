
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSplitter, QDockWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 
import sys
import random
from PyQt6.QtCore import QTimer, Qt
from queue import Queue
import math
import numpy as np
class LiveDataPlot(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.Backend = backend
        # Set up the main window
        self.setWindowTitle("Live Data Plotting with PyQt6")
        self.setGeometry(100, 100, 800, 600)
        self.allPlots = []

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Add a button to pause/resume
        self.pause_button = QPushButton("Stop")
        self.pause_button.setFixedSize(100,100)
        layout.addWidget(self.pause_button)

        # Create all charts from backend
        for chart in self.Backend.getChartObjects():
            plot = PlotWidget()
            layout.addWidget(plot)
            self.setup_plot(plot, chart.getTitle(), chart.getxLabel(), chart.getyLabel())
            plotDict = {}
            plotDict["plot"] = plot
            plotDict["chartId"] = chart.getId()
            plotDict["counter"] = 0
            plotDict["dataStream"] = {}
            colourCount = 0
            legend = pg.LegendItem(offset=(20, 10))
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
            self.allPlots.append(plotDict)
            dock = QDockWidget(chart.getTitle(), self)
            dock.setWidget(plot)
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.is_paused = False
        # Counter for x-axis
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # specifies how frequently the plot should be updated
        self.pause_button.clicked.connect(self.toggle_pause)

    def setup_plot(self, plot_widget, title, xLabel, yLabel):
        plot_widget.setBackground('w')
        plot_widget.setTitle(title, color="k", size="16pt")
        plot_widget.setLabel("left", yLabel, color="b", size="12pt")
        plot_widget.setLabel("bottom", xLabel, color="b", size="12pt")
      
    def toggle_pause(self):
        self.is_paused = not self.is_paused
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

class LiveHeatMap(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.Backend = backend
        self.setWindowTitle("Temperature Heatmap")
        self.setGeometry(100, 100, 600, 500)

        # Create main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Create ImageView for heatmap
        self.image_view = pg.ImageView()
        layout.addWidget(self.image_view)

        # Get relevant info
        self.sensorNum = 0
        for chart in self.Backend.getChartObjects():
            self.chart = chart
            self.sensors = sorted(chart.getSensors()) 
            self.numSensors = len(self.sensors)    
        self.N = int(math.sqrt(self.numSensors))

        # Create a colormap
        colormap = pg.colormap.get('inferno')  # Choose a color map
        lut = colormap.getLookupTable()  # Generate lookup table

        # Set the image with correct LUT
        self.image_item = self.image_view.getImageItem()  # Access the internal ImageItem
        self.image_item.setLookupTable(lut)  # Apply color map
        self.image_item.setLevels([20, 40])  # Set min-max temperature range

        #self.update_plot()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):
        # Get chart data
        data = [] #np.zeros((1, self.numSensors))
        for sensor in self.sensors:
            data.append(float(self.chart.getLastDataPoint(sensor)))
        structuredData = np.resize(np.array(data), (self.N,self.N))
        self.image_view.setImage(structuredData.T)
