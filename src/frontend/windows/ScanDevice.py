from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import Qt, QFont
from PySide6.QtCore import QTimer
from typing import Callable

from frontend.widgets.Loader import Loader
from frontend.windows.Devices import Devices
from frontend.windows.ScrollableWindow import ScrollableWindow


class ScanDevice(ScrollableWindow):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)
        self.title = QLabel("Scanning for Bluetooth Devices")
        self.loader = Loader(256)
        self.description = QLabel("Please wait for up to 5 seconds...")
        self.init_ui()

        self.trigger_bluetooth_scan()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_font = QFont()
        title_font.setPointSize(40)
        title_font.setWeight(QFont.Weight.DemiBold)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.loader.start_animation()
        layout.addWidget(self.loader)

        description_font = QFont()
        description_font.setPointSize(20)
        self.description.setFont(description_font)
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description)

        self.bind_scroll(layout)

    def trigger_bluetooth_scan(self):
        QTimer.singleShot(1000, self.on_scan_end)

    def on_scan_end(self):
        self.loader.stop_animation()
        dummy_data = [
            ("Arduino HC-06", "M9SK1K31-252D-43E3-A986-DCF3CB63D08", -50)
            for _ in range(33)
        ]
        dummy_data += [("long device name", "NDKA92N-24124-1241", -80)]

        self.switch_window(Devices(self.switch_window, dummy_data))
