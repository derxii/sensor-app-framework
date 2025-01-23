from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import Qt, QFont
from typing import Optional

class Button(QPushButton):
    def __init__(self, text: str, icon: Optional[str] = None, button_name: str = "",text_name: str = ""):
        super().__init__("")
        self.text = text
        self.icon = icon
        self.button_name = button_name
        self.text_name = text_name

        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.3)
        
        self.button_label = QLabel(text)

        self.init_ui()

    def init_ui(self):
        self.setObjectName(self.button_name)

        if self.icon:
            self.setIcon(self.icon)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_label.setObjectName(self.text_name)
        button_layout.addWidget(self.button_label)

        self.setLayout(button_layout)

    def add_text_font(self, text_font: QFont):
        self.button_label.setFont(text_font)

    def setDisabled(self, arg__1: bool):
        if arg__1:
            self.setGraphicsEffect(self.opacity)
        else:
            self.setEnabled(True)
        super().setDisabled(arg__1)


    def setEnabled(self, arg__1: bool):
        if arg__1:
            self.setGraphicsEffect(None)
        else:
            self.setDisabled(True)
        super().setEnabled(arg__1)