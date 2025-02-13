from PySide6.QtWidgets import  QWidget, QPushButton, QDockWidget, QGridLayout
from PySide6.QtCore import QTimer, Qt
from backend.LivePlots.LineChart import LineChart
from backend.LivePlots.Matrix import Matrix
from backend.LivePlots.Heatmap import Heatmap


class LiveDataPlot():
    # add central widget as an argument so that front end can call LiveDataPlot and embed docks in the layout
    def __init__(self, backend, window, layout):
        super().__init__()
        self.Backend = backend
        self.allCharts = []
        self.pause_button = QPushButton("Stop")
        self.pause_button.setFixedSize(70,70)
        self.controlsDock = QDockWidget("Controls", window)
        self.controlsDock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea| Qt.DockWidgetArea.LeftDockWidgetArea)
        controlsLayout = QGridLayout()
        controlsWidget = QWidget()
        controlsWidget.setObjectName("dock-container")
        controlsWidget.setLayout(controlsLayout)
        self.controlsDock.setWidget(controlsWidget)
        self.controlsDock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        controlsLayout.addWidget(self.pause_button)
        window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.controlsDock)

        # Create all line charts from backend
        for chart in self.Backend.getChartObjects():
            liveChart = None
            if chart.getType() == "line":
                liveChart = LineChart(window, layout, chart)
            elif chart.getType() == "matrix":
                liveChart = Matrix(window, layout, chart)
            elif chart.getType() == "heatmap":
                liveChart = Heatmap(window, chart)
                
            if liveChart is not None:
                self.allCharts.append(liveChart)

        self.is_paused = False
        self.counter = 0
        self.timer = QTimer()
        self.pause_button.clicked.connect(self.toggle_pause)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100) 
        
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.Backend.togglePause()
        self.pause_button.setText("Resume" if self.is_paused else "Stop")   
        
    def set_pause(self, val):
        self.is_paused = val
        self.pause_button.setText("Resume" if self.is_paused else "Stop")   

    def update_plot(self):
        if not self.is_paused:
            for liveChart in self.allCharts:
                liveChart.updatePlot()

    def clearPlots(self):
        for liveChart in self.allCharts:
            liveChart.clearPlot()
    
    def livePlotExists(self):
        return len(self.allCharts) != 0
    
    def hideControls(self):
        self.controlsDock.hide()

    def __del__(self):
        print("live dataplot deleted")
    
    def deleteAllData(self):
        self.allCharts = []