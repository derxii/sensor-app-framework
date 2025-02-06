from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import  Qt
from collections import Counter
from backend.DockObjects import SquareDockWidget

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

    def staticPlotExists(self):
        return self.chartCount != 0