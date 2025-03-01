from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import Qt, QFont, QIcon, QPixmap
from typing import Optional, Union


class Button(QPushButton):
    def __init__(
        self,
        text: str,
        icon_image_path: Optional[str] = None,
        button_name: str = "",
        text_name: str = "",
    ):
        super().__init__("")
        self.text = text
        self.icon: Union[QIcon, None] = None
        if icon_image_path:
            self.set_icon(icon_image_path)

        self.button_name = button_name
        self.text_name = text_name

        self.button_label = QLabel(text)

        self.init_ui()

    def init_ui(self):
        self.setObjectName(self.button_name)

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
            opacity = QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.55)
            self.setGraphicsEffect(opacity)
            super().setDisabled(arg__1)
        else:
            self.setEnabled(True)

    def setEnabled(self, arg__1: bool):
        if arg__1:
            self.setGraphicsEffect(None)
            super().setEnabled(arg__1)
        else:
            self.setDisabled(True)

    def set_icon(self, icon_image_path: str):
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(icon_image_path), QIcon.Mode.Normal)
        self.icon.addPixmap(QPixmap(icon_image_path), QIcon.Mode.Disabled)
        self.setIcon(self.icon)

    def change_text(self, text: str):
        self.text = text
        self.button_label.setText(text)

    def alter_name(self, button_name: str, text_name: str):
        self.button_name = button_name
        self.text_name = text_name
        self.set_name()

    def set_name(self):
        self.setObjectName(self.button_name)
        self.button_label.setObjectName(self.text_name)
