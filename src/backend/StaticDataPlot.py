from PySide6.QtWidgets import QVBoxLayout, QWidget, QDockWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
class StaticDataPlot():
    def __init__(self, backend, window):
        super().__init__()
        self.Backend = backend
        self.docks = []
        self.dockWeights = []
        self.chartCount = 0

        # Create Pie Series
        for chart in self.Backend.getChartObjects():
            if chart.getType() == "pie":
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
                dock.setWidget(widget)
                pieChartLayout = QVBoxLayout(widget)
                pieChartLayout.addWidget(chartView)
                window.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
                self.chartCount += 1

            if chart.getType() == "boxplot":
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

            if chart.getType() == "bar":

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
                


   

    def staticPlotExists(self):
        return self.chartCount != 0