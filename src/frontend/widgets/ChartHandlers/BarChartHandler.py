from typing import Union
from PySide6.QtWidgets import QWidget

from frontend.config import get_backend
from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormComponents.BinInputField import BinInputField
from frontend.widgets.FormComponents.FormUtils import create_text_input


class BarChartHandler(ChartHandler):
    def __init__(self):
        super().__init__()

        self.x_axis_label, self.x_axis_label_input = create_text_input("X-Axis Label")
        self.y_axis_label, self.y_axis_label_input = create_text_input("Y-Axis Label")

        self.bin_input = BinInputField()

    def get_custom_fields_container(self) -> QWidget:
        container, layout = self.create_basic_vertical_container()

        layout.addWidget(self.x_axis_label)
        layout.addWidget(self.y_axis_label)
        layout.addWidget(self.bin_input)

        container.setLayout(layout)
        return container

    def on_submit_create(
        self, title_text: str, sensors_selected: list[str]
    ) -> tuple[bool, Union[int, None]]:
        if len(self.bin_input.get_bin_values()) == 0:
            self.bin_input.set_no_bin_exception()
            return False, None

        id = get_backend().createChartObject(
            title_text,
            self.x_axis_label_input.text(),
            self.y_axis_label_input.text(),
            sensors_selected,
            "bar",
        )
        return True, id
