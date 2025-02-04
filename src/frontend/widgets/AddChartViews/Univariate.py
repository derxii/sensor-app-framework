from frontend.config import handle_exception
from frontend.widgets.AddChartViews.AddChartView import AddChartView

from frontend.widgets.ChartHandlers.LineChartHandler import LineChartHandler
from frontend.widgets.ChartHandlers.PieChartHandler import PieChartHandler


class Univariate(AddChartView):
    def __init__(self):
        super().__init__(
            {
                "Line": LineChartHandler,
                "Bar": LineChartHandler,
                "Histogram": LineChartHandler,
                "Pie": PieChartHandler,
                "Box-Plot": LineChartHandler,
            }
        )

        self.init_ui(True)

    def on_submit_create(self):
        sensors_selected = self.get_sensors_selected()
        if len(sensors_selected) != 1:
            handle_exception(
                Exception("No Sensors Selected"),
                None,
                False,
                "Please select a sensor.",
            )
            return False, None

        return self.chart_handler.on_submit_create(
            self.title_input.text(), sensors_selected
        )
