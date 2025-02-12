from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Histogram():
    def __init__(self, chart, window):
        dictData = chart.getAllData()
        data = []
        allData = []
        for sensor in dictData.keys():
            data.append([float(val) for val in dictData[sensor]])
            allData += dictData[sensor]
        widget = QWidget()
        widget.setObjectName("dock-container")
        chartFigure = Figure()
        chartCanvas = FigureCanvas(chartFigure)
        counter =Counter(allData)
        bins = counter.keys()
        axis = chartFigure.add_subplot()
        axis.hist(data, bins=len(bins),color='blue', edgecolor='black')
        axis.set_title(chart.getTitle())
        axis.set(xlabel=chart.getxLabel(), ylabel=chart.getyLabel())
        layout = QVBoxLayout()
        layout.addWidget(chartCanvas)
        widget.setLayout(layout)
        dock = QDockWidget(chart.getTitle(), window)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        dock.setWidget(widget)
        window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)