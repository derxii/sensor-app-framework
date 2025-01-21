from typing import Callable
from PySide6.QtWidgets import (
    QPushButton,
    QGraphicsDropShadowEffect,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QFont

from frontend.config import dynamically_repaint_widget, enable_custom_styling


class ResetButton(QWidget):
    def __init__(self, is_simple: bool, switch_window: Callable[[QWidget], None]):
        super().__init__()
        self.is_simple = is_simple
        self.switch_window = switch_window

        text = "Restart Setup"
        if is_simple:
            self.button = QPushButton(text)
            self.init_ui()
            self.init_ui_simple()
        else:
            text = text.upper()
            self.button = QPushButton(text)
            self.init_ui()
            self.init_ui_complex()

        self.button.clicked.connect(self.on_click)

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setWeight(QFont.Weight.DemiBold)
        self.button.setFont(font)

    def init_ui_simple(self):
        self.set_shadow()
        self.button.setObjectName("reset-button-simple")
        self.layout.addWidget(self.button)
        self.button.setMinimumWidth(150)

    def set_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setOffset(0, 0)

        self.setGraphicsEffect(shadow)

    def init_ui_complex(self):
        pass

    def paintEvent(self, _):
        enable_custom_styling(self)

    def on_click(self):
        from frontend.windows.Welcome import Welcome

        self.switch_window(Welcome(self.switch_window))

    def disable_button(self):
        self.button.setObjectName("disabled")
        self.setGraphicsEffect(None)
        dynamically_repaint_widget(self, self.button)

    def enable_button(self):
        self.set_shadow()
        self.button.setObjectName("reset-button-simple")
        dynamically_repaint_widget(self, self.button)
