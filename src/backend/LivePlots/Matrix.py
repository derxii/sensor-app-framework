from PySide6.QtWidgets import QVBoxLayout, QWidget, QGridLayout
import pyqtgraph as pg 
from PySide6.QtCore import Qt
import math
import numpy as np
from backend.DockObjects import SquareDockWidget, on_change_level

class Matrix():
    def __init__(self, window, layout, chart):
        self.chart = chart
        dock = SquareDockWidget(chart.getTitle(), window)
        dock.setLayout(layout)
        widget = QWidget()
        widget.setObjectName("dock-container")
        dock.topLevelChanged.connect(lambda floating: on_change_level(floating, widget))
        dock.setWidget(widget)
        dock.resize(150,150)
        matrixLayout = QGridLayout(widget) #QVBoxLayout(widget)
        imageView = pg.ImageView()
        imageView = pg.ImageView()
        matrixLayout.addWidget(imageView)

        colormap = pg.colormap.get('turbo') 
        lut = colormap.getLookupTable() 
        image_item = imageView.getImageItem()  
        image_item.setLookupTable(lut)  
        imageView.setColorMap(colormap)
        rangeVals = chart.getMinMaxRange()
        if rangeVals is not None:
            (min, max) = rangeVals
            image_item.setLevels([min, max]) 

        sensors = sorted(chart.getSensors())
        matrixDict = {"chartId":chart.getId(), "imageView": imageView, "sensors": sensors , "numSensors": len(sensors), "N": int(math.sqrt(len(sensors)))}
        self.matrixDict = matrixDict
        window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dock)

    def updatePlot(self):
        data = [] 
        if self.chart.isQueueReady() is False:
            return
        for sensor in self.matrixDict["sensors"]:
            data.append(float(self.chart.getLastDataPoint(sensor)))
        structuredData = np.resize(np.array(data), (self.matrixDict["N"], self.matrixDict["N"]))
        self.matrixDict["imageView"].setImage(structuredData.T)

    def clearPlot(self):
        data = np.zeros((self.matrixDict["N"], self.matrixDict["N"]), dtype=float)
        self.matrixDict["imageView"].setImage(data.T)
