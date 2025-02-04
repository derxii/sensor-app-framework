from typing import Union
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLayout
from abc import abstractmethod


class ChartHandler(QWidget):
    @abstractmethod
    def get_custom_fields_container(self) -> QWidget:
        pass

    @abstractmethod
    def on_submit_create(
        self, title_text: str, sensors_selected: list[str]
    ) -> tuple[bool, Union[int, None]]:
        pass

    def create_basic_vertical_container(self) -> tuple[QWidget, QLayout]:
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        return container, layout
