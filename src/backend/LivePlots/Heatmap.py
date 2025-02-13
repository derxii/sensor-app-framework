from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget, QGridLayout
import pyqtgraph as pg 
from PySide6.QtCore import Qt
import numpy as np

from backend.DockObjects import on_change_level

class Heatmap():
    def __init__(self, window, chart):
        self.chart = chart
        dock = QDockWidget(chart.getTitle(), window)
        widget = QWidget()
        widget.setObjectName("dock-container")
        dock.topLevelChanged.connect(lambda floating: on_change_level(floating, widget))
        dock.setWidget(widget)
        heatmapLayout = QGridLayout(widget) #QVBoxLayout(widget)
        plot_item = pg.PlotItem()
        imageView = pg.ImageView()
        imageView = pg.ImageView(view=plot_item)
        heatmapLayout.addWidget(imageView)
        colormap = pg.colormap.get('viridis') 
        lut = colormap.getLookupTable() 
        imageView.setColorMap(colormap)
        image_item = imageView.getImageItem()  
        image_item.setLookupTable(lut) 
        rangeVals = chart.getMinMaxRange()
        if rangeVals is not None:
            (min, max) = rangeVals
            image_item.setLevels([min, max]) 
        categories = chart.getCategories()
        sensors = sorted(chart.getSensors())
        
        plot_item.setLabel('left', chart.getyLabel())
        plot_item.setLabel('bottom', chart.getxLabel())
        x_ticks = [(i, sensors[i]) for i in range(len(sensors))]
        y_ticks = [(i, f"{categories[i][0]}-{categories[i][1]}") for i in range(len(categories))]
        plot_item.getAxis('bottom').setTicks([x_ticks])
        plot_item.getAxis('left').setTicks([y_ticks])

        dataStruct = np.zeros((len(categories), len(sensors)), dtype=float)
        self.heatmapDict = {"chartId":chart.getId(), "imageView": imageView, "sensors": sensors , "numSensors": len(sensors), "categories": categories, "numCategories": len(categories), "data": dataStruct}
        window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,dock)

    def updatePlot(self):
        categories = self.heatmapDict["categories"]
        sensors = self.heatmapDict["sensors"]
        data = self.heatmapDict["data"]
        chartId = int(self.heatmapDict["chartId"])
        if self.chart.isQueueReady() is False:
            return
        for j in range(0, len(sensors)):
            dataVal = self.chart.getLastDataPoint(sensors[j])
            if dataVal is None:
                continue
            dataVal = float(dataVal)
            for k in range(0, len(categories)):
                if dataVal >= categories[k][0] and dataVal <= categories[k][1]:
                    data[k][j] += 1
        self.heatmapDict["data"] = data
        self.heatmapDict["imageView"].setImage(data.T)

    def clearPlot(self):
        self.heatmapDict["data"] =  np.zeros((self.heatmapDict["numCategories"], self.heatmapDict["numSensors"]), dtype=float)