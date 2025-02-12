from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QDockWidget, QGridLayout
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg 
from PySide6.QtCore import QTimer, Qt
import math
import numpy as np
from backend.DockObjects import SquareDockWidget

class LineChart():
    def __init__(self, window, layout, chart):
        self.chart = chart
        #self.Backend = backend
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
        #self.allPlots.append(plotDict)
        dock = QDockWidget(chart.getTitle(), window)
        plot.setObjectName("dock-container")
        dock.setWidget(plot)
        window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.plotDict = plotDict

    def setup_plot(self, plot_widget, title, xLabel, yLabel):
        plot_widget.setBackground('w')
        plot_widget.setTitle(title, color="k", size="16pt")
        plot_widget.setLabel("left", yLabel, color="b", size="12pt")
        plot_widget.setLabel("bottom", xLabel, color="b", size="12pt")

    def updatePlot(self):
        for sensor in self.plotDict["dataStream"].keys(): 
            dataDict = self.chart.getRecentData()
            dataLength = dataDict[sensor].qsize()
            plotLine = self.plotDict["dataStream"][sensor]["line"]
            for j in range(0, dataLength):
                val = float(dataDict[sensor].get())
                self.plotDict["dataStream"][sensor]["yData"].append(val)
                self.plotDict["dataStream"][sensor]["counter"] += 1
                self.plotDict["dataStream"][sensor]["xData"].append(self.plotDict["dataStream"][sensor]["counter"])

            plotLine.setData(self.plotDict["dataStream"][sensor]["xData"], self.plotDict["dataStream"][sensor]["yData"])
            self.plotDict["dataStream"][sensor]["line"] = plotLine

    def clearPlot(self):
        for sensor in self.plotDict["dataStream"].keys(): 
            self.plotDict["dataStream"][sensor]["yData"] = []
            self.plotDict["dataStream"][sensor]["counter"] = 0
            self.plotDict["dataStream"][sensor]["xData"] = []
            plotLine = self.plotDict["dataStream"][sensor]["line"]
            plotLine.setData(self.plotDict["dataStream"][sensor]["xData"], self.plotDict["dataStream"][sensor]["yData"])
            self.plotDict["dataStream"][sensor]["line"] = plotLine
