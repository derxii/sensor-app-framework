from frontend.config import handle_exception
from frontend.widgets.AddChartViews.AddChartView import AddChartView

from frontend.widgets.ChartHandlers.HeatmapMatrixHandler import HeatmapMatrixHandler
from frontend.widgets.ChartHandlers.LineChartHandler import LineChartHandler


class Multivariate(AddChartView):
    def __init__(self):
        super().__init__(
            {
                "Line": LineChartHandler,
                "Heatmap Matrix (Sensors vs. Values)": HeatmapMatrixHandler,
            }
        )

        self.init_ui(False)

    def on_submit_create(self):
        sensors_selected = self.get_sensors_selected()

        if len(sensors_selected) == 0:
            handle_exception(
                Exception("Sensors Not Selected"),
                None,
                False,
                "At least one sensor must be selected.",
            )
            return False, None

        return self.chart_handler.on_submit_create(
            self.title_input.text(), sensors_selected
        )
