from typing import Union
from PySide6.QtWidgets import QWidget

from frontend.config import get_backend
from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormUtils import create_text_input


class HeatmapMatrixHandler(ChartHandler):
    def __init__(self):
        super().__init__()

        self.y_axis_label, self.y_axis_label_input = create_text_input("Y-Axis Label")

    def get_custom_fields_container(self) -> QWidget:
        container, layout = self.create_basic_vertical_container()

        layout.addWidget(self.y_axis_label)

        container.setLayout(layout)
        return container

    def on_submit_create(
        self, title_text: str, sensors_selected: list[str]
    ) -> tuple[bool, Union[int, None]]:
        id = get_backend().createChartObject(
            title_text,
            "",
            self.y_axis_label_input.text(),
            sensors_selected,
            "heatmap",
        )
        return True, id
