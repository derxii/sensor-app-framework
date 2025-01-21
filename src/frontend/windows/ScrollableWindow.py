from typing import Callable
from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLayout


class ScrollableWindow(QWidget):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__()

        self.switch_window = switch_window

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.container.setObjectName("scrollable-window")

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

    def bind_scroll(self, contained_layout: QLayout):
        self.container.setLayout(contained_layout)
        self.scroll_area.setWidget(self.container)
