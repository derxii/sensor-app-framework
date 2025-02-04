from typing import Union
from PySide6.QtWidgets import QWidget

from frontend.config import get_backend, handle_exception
from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormComponents.BinInputField import BinInputField


class PieChartHandler(ChartHandler):
    def __init__(self):
        super().__init__()

        self.bin_input = BinInputField()

    def get_custom_fields_container(self) -> QWidget:
        container, layout = self.create_basic_vertical_container()

        layout.addWidget(self.bin_input)

        container.setLayout(layout)
        return container

    def on_submit_create(
        self, title_text: str, sensors_selected: list[str]
    ) -> tuple[bool, Union[int, None]]:
        if len(self.bin_input.get_bin_values()) == 0:
            handle_exception(
                Exception("Not Enough Bins"), None, None, "Please add at least one bin."
            )
            return False, None

        id = get_backend().createChartObject(
            title_text,
            "",
            "",
            sensors_selected,
            "pie",
        )
        return True, id
