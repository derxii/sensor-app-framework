from PySide6.QtWidgets import QVBoxLayout, QWidget
from typing import Callable

from frontend.widgets.ScrollableWindow import ScrollableWindow

class ScanDevice(ScrollableWindow):

    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.bind_scroll(layout)