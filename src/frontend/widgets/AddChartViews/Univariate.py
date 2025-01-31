from frontend.config import handle_exception
from frontend.widgets.AddChartViews.AddChartView import AddChartView

from frontend.widgets.ChartHandlers.LineChartHandler import LineChartHandler


class Univariate(AddChartView):
    def __init__(self):
        super().__init__(
            {
                "Line": LineChartHandler,
                "Bar": LineChartHandler,
                "Histogram": LineChartHandler,
                "Pie": LineChartHandler,
                "Box-Plot": LineChartHandler,
            }
        )

        self.init_ui(True)

    def on_submit_create(self):
        sensors_selected = self.get_sensors_selected()
        if len(sensors_selected) != 1:
            handle_exception(
                Exception("Incorrect Amount of Sensors Selected"),
                None,
                False,
                "Only one sensor can be selected.",
            )
            return False, None

        return self.chart_handler.on_submit_create(
            self.title_input.text(), sensors_selected
        )
