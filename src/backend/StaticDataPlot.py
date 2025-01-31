import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDockWidget, QGridLayout
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QTimer, Qt

class StaticDataPlot(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.Backend = backend
        self.docks = []
        self.dockWeights = []
        # Create the main window
        self.setWindowTitle("Static plots")
        self.setGeometry(100, 100, 800, 600)


        # Create Pie Series
        for chart in self.Backend.getChartObjects():
            if chart.getType() == "pie":
                dictData = chart.getAllData()
                allData = []
                for sensor in dictData.keys():
                    allData += dictData[sensor]
                catagories = set(allData)
                series = QPieSeries()
                for item in catagories:
                    series.append(item, allData.count(item))
                
                # Highlight the largest slice
                largestSlice = max(series.slices(), key=lambda s: s.percentage())
                largestSlice.setExploded(True)  # Pull the largest slice out
                largestSlice.setLabelVisible(True)  # Show the label

                # Create Chart
                qchart = QChart()
                qchart.addSeries(series)
                qchart.setTitle(chart.getTitle())

                # Create Chart View
                chartView = QChartView(qchart)
                chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

                # Set Layout
                dock = QDockWidget(str(chart.getId()), self)
                widget = QWidget()
                dock.setWidget(widget)
                pieChartLayout = QVBoxLayout(widget)
                pieChartLayout.addWidget(chartView)
                self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)


