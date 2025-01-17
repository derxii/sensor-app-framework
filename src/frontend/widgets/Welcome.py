from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PySide6.QtGui import Qt, QFont, QIcon
from PySide6.QtCore import QSize
from typing import Callable

from frontend.helper import get_image_path
from frontend.widgets.ScanDevice import ScanDevice
from frontend.widgets.ScrollableWindow import ScrollableWindow

class Welcome(ScrollableWindow):

    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)

        self.title = QLabel("Sensor Data Visualiser")
        self.logo = QLabel()
        self.description = QLabel("Visualise your sensor data in real time using " + 
                                  "custom charts via a Bluetooth connection.")
        self.connect_button = QPushButton()
        self.connect_button_label = QLabel("Scan Bluetooth Devices")

        self.connect_button.clicked.connect(lambda: self.switch_window(ScanDevice(self.switch_window)))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont()
        title_font.setWeight(QFont.Weight.Medium)
        title_font.setPointSize(40)

        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.title)

        image = QIcon(get_image_path("icon.svg")).pixmap(QSize(256, 256))
        self.logo.setPixmap(image)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.logo)

        description_font = QFont()
        description_font.setPointSize(20)

        self.description.setFont(description_font)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.description)

        layout.addSpacing(20)

        self.connect_button.setObjectName("connect-button")
        self.connect_button.setMinimumHeight(40)
        self.connect_button.setIcon(QIcon(get_image_path("bluetooth.svg")))
        self.connect_button.setIconSize(QSize(24, 24))

        button_layout = QHBoxLayout()
        self.connect_button_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.connect_button_label.setObjectName("connect-text")
        font = QFont()
        font.setPointSize(20)
        font.setWeight(QFont.Weight.Medium)
        self.connect_button_label.setFont(font)

        button_layout.addWidget(self.connect_button_label)

        self.connect_button.setLayout(button_layout)
        layout.addWidget(self.connect_button)

        self.bind_scroll(layout)