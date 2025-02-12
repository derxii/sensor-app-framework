from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class BarChart():
    def __init__(self, chart, window):
        dictData = chart.getAllData()
        allData = []
        # Add all data to a single list
        for sensor in dictData.keys():
            allData += dictData[sensor]
        categories = chart.getCategories()

        # If no categories are given then each data value is its own category
        categoryLabels = []
        countData = []
        if len(categories) == 0:
            counter = Counter(allData)
            for (category, count) in counter.items():
                countData.append(count)
                categoryLabels.append(category)
        else:
            for (low, high) in categories:
                filteredData = list(filter(lambda val:float(val) >= low and float(val) <= high, allData))
                categoryString = f"{low}-{high}"
                countData.append(len(filteredData))
                categoryLabels.append(categoryString)
        widget = QWidget()
        widget.setObjectName("dock-container")
        chartFigure = Figure()
        chartCanvas = FigureCanvas(chartFigure)
        axis = chartFigure.add_subplot()
        axis.bar(categoryLabels, countData)
        axis.set_title(chart.getTitle())
        axis.set(xlabel=chart.getxLabel(), ylabel=chart.getyLabel())
        layout = QVBoxLayout()
        layout.addWidget(chartCanvas)
        widget.setLayout(layout)
        dock = QDockWidget(chart.getTitle(), window)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        dock.setWidget(widget)
        window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)