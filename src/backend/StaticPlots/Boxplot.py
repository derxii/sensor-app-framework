from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Boxplot():
    def __init__(self, chart, window):
        widget = QWidget()
        chartFigure = Figure()
        chartCanvas = FigureCanvas(chartFigure)
        dictData = chart.getAllData()
        data = []
        for sensor in dictData.keys():
            data.append([float(val) for val in dictData[sensor]])
                
        axis = chartFigure.add_subplot() # adds subplot in the first index position
        axis.boxplot(data)
        axis.set_title(chart.getTitle())
        # Add sensor labels to x axis
        axis.set_xticklabels(dictData.keys())
        # Add y label to y axis
        axis.set(ylabel=chart.getyLabel())
        layout = QVBoxLayout()
        layout.addWidget(chartCanvas)
        widget.setLayout(layout)
        dock = QDockWidget(chart.getTitle(), window)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        dock.setWidget(widget)
        window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)