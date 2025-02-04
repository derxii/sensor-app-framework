from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import Qt, QFont, QIcon
from PySide6.QtCore import QSize
from typing import Callable

from frontend.config import get_image_path
from frontend.widgets.Button import Button
from frontend.windows.ScanDevice import ScanDevice
from frontend.windows.ScrollableWindow import ScrollableWindow


class Welcome(ScrollableWindow):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)

        self.title = QLabel("Sensor Data Visualiser")
        self.logo = QLabel()
        self.description = QLabel(
            "Visualise your sensor data in real time using "
            + "custom charts via a Bluetooth connection."
        )

        self.connect_button = Button(
            "Scan Bluetooth Devices",
            get_image_path("bluetooth.svg"),
            "scan-button",
            "white",
        )

        self.connect_button.clicked.connect(
            lambda: self.switch_window(ScanDevice(self.switch_window))
        )
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_font = QFont()
        title_font.setWeight(QFont.Weight.DemiBold)
        title_font.setPointSize(40)

        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title, 3)

        image = QIcon(get_image_path("icon.svg")).pixmap(QSize(256, 256))
        self.logo.setPixmap(image)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo, 5)

        description_font = QFont()
        description_font.setPointSize(20)

        self.description.setFont(description_font)
        self.description.setWordWrap(True)
        self.description.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        )
        layout.addWidget(self.description, 1)

        layout.addSpacing(20)

        self.connect_button.setMinimumHeight(40)
        self.connect_button.setIconSize(QSize(24, 24))

        font = QFont()
        font.setPointSize(20)
        font.setWeight(QFont.Weight.DemiBold)
        self.connect_button.add_text_font(font)

        layout.addWidget(self.connect_button)
        layout.addSpacing(40)

        self.bind_scroll(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        title_font = QFont()
        title_font.setWeight(QFont.Weight.DemiBold)
        title_font.setPointSizeF(min(int(min(self.width(), self.height()) * 0.08), 100))

        self.title.setFont(title_font)

        size = min(int(min(self.width(), self.height()) * 0.45), 512)
        image = QIcon(get_image_path("icon.svg")).pixmap(QSize(size, size))
        self.logo.setPixmap(image)
