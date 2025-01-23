from typing import Callable
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize

from frontend.config import enable_custom_styling, get_image_path
from frontend.widgets.Button import Button


class ResetButton(QWidget):
    def __init__(self, is_icon: bool, switch_window: Callable[[QWidget], None]):
        super().__init__()
        self.is_simple = is_icon
        self.switch_window = switch_window

        text = "Restart Setup"
        if is_icon:
            self.button = Button(text, None, "reset-button-simple", "red")
            self.init_ui()
            self.init_ui_simple()
        else:
            text = text.upper()
            self.button = Button(
                text, get_image_path("configure.svg"), "reset-button-icon", "red"
            )
            self.button.setIconSize(QSize(28, 28))
            self.init_ui()
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(self.button)

        self.button.clicked.connect(self.on_click)

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setWeight(QFont.Weight.DemiBold)
        self.button.add_text_font(font)

    def init_ui_simple(self):
        self.set_shadow()
        self.layout.addWidget(self.button)
        self.button.setMinimumWidth(150)

    def set_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setOffset(0, 0)

        self.setGraphicsEffect(shadow)

    def paintEvent(self, _):
        enable_custom_styling(self)

    def on_click(self):
        from frontend.windows.Welcome import Welcome

        self.switch_window(Welcome(self.switch_window))

    def disable_button(self):
        if self.is_simple:
            self.setGraphicsEffect(None)
        self.button.setDisabled(True)

    def enable_button(self):
        if self.is_simple:
            self.set_shadow()
        self.button.setEnabled(True)
