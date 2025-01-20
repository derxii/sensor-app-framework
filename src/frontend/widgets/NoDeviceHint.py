from typing import Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import Qt, QFont

from frontend.widgets.ResetButton import ResetButton


class NoDeviceHint(QWidget):
    def __init__(self, switch_window: Callable[[QWidget], None]):

        super().__init__()
        self.hint = QLabel("Select a Bluetooth device to show more information.")
        self.reset_button = ResetButton(True, switch_window)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        top_container = QWidget()
        top_layout = QVBoxLayout()
        top_container.setLayout(top_layout)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_container.setContentsMargins(0, 0, 0, 0)

        hint_font = QFont()
        hint_font.setPointSizeF(18)
        hint_font.setItalic(True)
        hint_font.setWeight(QFont.Weight.Light)
        self.hint.setFont(hint_font)

        top_layout.addWidget(self.hint)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(top_container, 12)

        bottom_container = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_container.setLayout(bottom_layout)

        bottom_layout.addWidget(self.reset_button)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

        layout.addWidget(bottom_container, 1)
        self.setLayout(layout)
