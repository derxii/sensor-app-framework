from typing import Callable
from PySide6.QtWidgets import QComboBox, QWidget, QLabel
from PySide6.QtGui import QFont


from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormComponents.FormUtils import (
    get_form_font,
    set_left_right_aligned_widgets,
)


class TypeSelector(QComboBox):
    def __init__(
        self,
        text_chart_handler_mapping: dict[str, ChartHandler],
        switch_chart_handler: Callable[[ChartHandler], None],
    ):
        super().__init__()

        self.text_chart_handler_mapping = text_chart_handler_mapping
        self.switch_chart_handler = switch_chart_handler

        for item in text_chart_handler_mapping.keys():
            self.addItem(item)

        self.currentTextChanged.connect(self.change_chart_handler)
        self.init_ui()

    def init_ui(self):
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

    def create_type_selector_form_container(
        text_chart_handler_mapping: dict[str, ChartHandler],
        switch_chart_handler: Callable[[ChartHandler], None],
    ) -> QWidget:
        label = QLabel("Chart Type: ")
        label.setFont(get_form_font())

        type_selector = TypeSelector(text_chart_handler_mapping, switch_chart_handler)
        return set_left_right_aligned_widgets(label, type_selector, 9, 4)

    def change_chart_handler(self):
        self.switch_chart_handler(self.text_chart_handler_mapping[self.currentText()]())
