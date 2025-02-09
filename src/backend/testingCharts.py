'''import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import  Qt
class BoxPlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Generate sample data
        data = [np.random.normal(0, std, 100) for std in range(1, 5)]
        print(data)
        
        # Create a box plot
        ax = self.figure.add_subplot(111)
        ax.boxplot(data)
        ax.set_title("Box Plot Example")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box Plot with QDockWidget")

        # Create a QDockWidget
        self.dock = QDockWidget("Box Plot", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        # Create the BoxPlotWidget and set it as the dock's widget
        self.box_plot_widget = BoxPlotWidget()
        self.dock.setWidget(self.box_plot_widget)

        # Add the dock to the main window
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())'''
'''
import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PySide6.QtCore import  Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Generate sample data
        categories = ['A', 'B', 'C', 'D', 'E']
        values = np.random.randint(5, 20, size=len(categories))  # Random values

        # Create a bar chart
        ax = self.figure.add_subplot(111)
        ax.bar(categories, values, color=['blue', 'green', 'red', 'purple', 'orange'])
        ax.set_title("Bar Chart Example")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bar Chart with QDockWidget")

        # Create a QDockWidget
        self.dock = QDockWidget("Bar Chart", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        # Create the BarChartWidget and set it as the dock's widget
        self.bar_chart_widget = BarChartWidget()
        self.dock.setWidget(self.bar_chart_widget)

        # Add the dock to the main window
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
'''

import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HistogramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Generate sample data
        data = np.random.randn(1000)  # 1000 random points from a normal distribution
        
        # Create a histogram
        ax = self.figure.add_subplot(111)
        ax.hist(data, bins=30, color='blue', edgecolor='black', alpha=0.7)
        ax.set_title("Histogram Example")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram with QDockWidget")

        # Create a QDockWidget
        self.dock = QDockWidget("Histogram", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea  | Qt.DockWidgetArea.RightDockWidgetArea )

        # Create the HistogramWidget and set it as the dock's widget
        self.histogram_widget = HistogramWidget()
        self.dock.setWidget(self.histogram_widget)

        # Add the dock to the main window
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea , self.dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

