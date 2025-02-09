from backend.StaticPlots.PieChart import PieChart
from backend.StaticPlots.BarChart import BarChart
from backend.StaticPlots.Histogram import Histogram
from backend.StaticPlots.Boxplot import Boxplot
class StaticDataPlot():
    def __init__(self, backend, window):
        super().__init__()
        self.Backend = backend
        self.docks = []
        self.dockWeights = []
        self.chartCount = 0
        self.plots = []

        # Create Pie Series
        for chart in self.Backend.getChartObjects():
            plot = None
            chartType = chart.getType()
            if chartType == "pie":
                plot = PieChart(chart, window)
            elif chartType == "boxplot":
                plot = Boxplot(chart, window)
            elif chartType== "bar":
                plot = BarChart(chart, window)
            elif chartType == "histogram":
                plot = Histogram(chart, window)

            if plot is not None:
                self.plots.append(plot)
            
    def staticPlotExists(self):
        return len(self.plots) != 0