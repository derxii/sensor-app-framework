import asyncio
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import Qt, QFont
from PySide6.QtCore import QTimer
from typing import Callable

from frontend.config import get_backend, get_debug_scan_devices, is_debug
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

        # Delay to ensure button is responsive
        QTimer.singleShot(50, self.trigger_bluetooth_scan)

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
        if is_debug():
            QTimer.singleShot(0, lambda: self.on_scan_end([]))
        else:
            asyncio.ensure_future(self.process_scan_response())

    async def process_scan_response(self):
        scan_response = await get_backend().scanForDevices()
        self.on_scan_end(scan_response)

    def on_scan_end(self, data: list[tuple[str, str, int]]):
        self.loader.stop_animation()
        if is_debug():
            data = get_debug_scan_devices()

        self.switch_window(
            Devices(self.switch_window, sorted(data, key=lambda d: (-d[2], d[0])))
        )
