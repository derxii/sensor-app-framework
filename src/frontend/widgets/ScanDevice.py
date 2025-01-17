from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QMovie, Qt, QFont
from PySide6.QtCore import QSize, QTimer
from typing import Callable

from frontend.helper import get_image_path
from frontend.widgets.ScrollableWindow import ScrollableWindow

class ScanDevice(ScrollableWindow):

    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)
        self.title = QLabel("Scanning for Bluetooth Devices")
        self.loading_animation = QLabel()
        self.movie = QMovie(get_image_path("spinner.gif"))
        self.description = QLabel("Please wait for up to 5 seconds...")
        self.init_ui()

        self.trigger_bluetooth_scan()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_font = QFont()
        title_font.setPointSize(40)
        title_font.setWeight(QFont.Weight.Medium)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.movie.setScaledSize(QSize(256, 256))
        self.loading_animation.setMovie(self.movie)
        self.movie.start()
        self.loading_animation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.loading_animation)

        description_font = QFont()
        description_font.setPointSize(20)
        self.description.setFont(description_font)
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description)

        self.bind_scroll(layout)

    def trigger_bluetooth_scan(self):
        QTimer.singleShot(5000, self.on_scan_end)

    def on_scan_end(self):
        self.movie.stop()