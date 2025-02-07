from typing import Union
from PySide6.QtWidgets import QWidget

from frontend.config import get_backend
from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormComponents.FormUtils import create_text_input
from frontend.widgets.FormComponents.RangeInput import RangeInput


class MatrixHandler(ChartHandler):
    def __init__(self):
        super().__init__()

        self.y_axis_label, self.y_axis_label_input = create_text_input("Y-Axis Label")
        self.range_container, self.range_input = RangeInput.create_range_input()

    def get_custom_fields_container(self) -> QWidget:
        container, layout = self.create_basic_vertical_container()

        layout.addWidget(self.y_axis_label)
        layout.addWidget(self.range_container)

        container.setLayout(layout)
        return container

    def on_submit_create(
        self, title_text: str, sensors_selected: list[str]
    ) -> tuple[bool, Union[int, None]]:
        result = self.range_input.get_bin_value()
        if result is None:
            return False, None

        lower_value, upper_value = result
        print(result)
        id = get_backend().createChartObject(
            title_text,
            "",
            self.y_axis_label_input.text(),
            sensors_selected,
            "matrix",
        )
       
        return True, id
