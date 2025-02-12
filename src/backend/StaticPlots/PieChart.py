from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class PieChart():
    def __init__(self, chart, window):
        dictData = chart.getAllData()
        allData = []
        for sensor in dictData.keys():
            allData += dictData[sensor]
        categories = chart.getCategories()
        series = QPieSeries()
        if len(categories) == 0:
            counter = Counter(allData)
            for (category, count) in counter.items():
                series.append(category, count)
        else:
            for (low, high) in categories:
                filteredData = list(filter(lambda val:float(val) >= low and float(val) <= high, allData))
                categoryString = f"{low}-{high}"
                series.append(categoryString, len(filteredData))
        for slice in series.slices():
            percentage = slice.percentage()
            slice.setLabel(f"{slice.label()}: {str(round(percentage*100, 2))}%")
            slice.setLabelVisible(True)
        # Create Chart
        qchart = QChart()
        qchart.addSeries(series)
        qchart.setTitle(chart.getTitle())

        # Create Chart View
        chartView = QChartView(qchart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)
        dock = SquareDockWidget(chart.getTitle(), window) 
        widget = QWidget()
        widget.setObjectName("dock-container")
        dock.setWidget(widget)
        pieChartLayout = QVBoxLayout(widget)
        pieChartLayout.addWidget(chartView)
        window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)