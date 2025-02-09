import math
from typing import Callable, Optional
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QSystemTrayIcon,
    QMessageBox,
)
from PySide6.QtGui import QFont, Qt, QIcon
from PySide6.QtCore import QSize, QTimer, QThread

from frontend.config import (
    get_backend,
    get_image_path,
    get_virtual_port,
    handle_exception,
    is_debug,
)
from frontend.thread.Worker import Worker
from frontend.widgets.Button import Button
from frontend.widgets.Loader import Loader
from frontend.widgets.ResetButton import ResetButton
from frontend.windows.Dashboard import Dashboard
from frontend.windows.ScrollableWindow import ScrollableWindow


class DeviceDetailed(ScrollableWindow):
    def __init__(
        self,
        name: str,
        address: str,
        rssi: int,
        switch_window: Callable[[QWidget], None],
        set_press_device_enabled: Callable[[bool], None],
    ):
        super().__init__(switch_window)
        self.name = QLabel(name)
        self.address = QLabel(address)
        self.rssi = QLabel(f"{'Unknown ' if math.isinf(rssi) else rssi}dBm")
        self.set_press_device_enabled = set_press_device_enabled

        self.thread = QThread()

        strength_text, strength_image = self.get_strength_from_rssi(rssi)
        self.signal_strength = QLabel(strength_text)
        if strength_image:
            self.signal_image = QLabel()
            image = QIcon(get_image_path(strength_image)).pixmap(QSize(16, 16))
            self.signal_image.setPixmap(image)
        else:
            self.signal_image = None

        self.loader = Loader(200)

        self.restart_button = ResetButton(True, self.switch_window)
        self.connect_button = Button("Connect", None, "connect-button", "white")
        self.connect_button.clicked.connect(self.connect)

        self.error_message = "Please ensure your device is paired and sending data in the correct format. If errors continue, check your Bluetooth connection."

        self.init_ui()

    def init_ui(self):
        root_layout = QVBoxLayout()

        name_font = QFont()
        name_font.setPointSizeF(32)
        name_font.setWeight(QFont.Weight.DemiBold)
        self.name.setFont(name_font)
        self.name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name.setContentsMargins(0, 0, 0, 0)
        self.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        root_layout.setContentsMargins(0, 0, 0, 0)

        root_layout.addWidget(self.name)

        root_layout.addSpacing(20)

        root_layout.addWidget(
            self.create_left_right_aligned_text(self.address, "Address")
        )
        root_layout.addWidget(self.create_left_right_aligned_text(self.rssi, "RSSI"))
        root_layout.addWidget(
            self.create_left_right_aligned_text(
                self.signal_strength, "Signal Strength", self.signal_image
            )
        )

        root_layout.addWidget(self.loader, 3)

        bottom_container = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(9, 0, 9, 0)
        bottom_layout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )

        connect_font = QFont()
        connect_font.setWeight(QFont.Weight.DemiBold)
        self.connect_button.add_text_font(connect_font)
        self.connect_button.setMinimumWidth(150)

        bottom_layout.addWidget(self.restart_button)
        bottom_layout.addWidget(self.connect_button)

        bottom_container.setLayout(bottom_layout)

        root_layout.addWidget(bottom_container, 1)

        self.bind_scroll(root_layout)

    def create_left_right_aligned_text(
        self, text: QLabel, label: str, image: Optional[QLabel] = None
    ):
        container = QWidget()
        container.setMaximumHeight(40)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout()

        font = QFont()
        font.setPointSizeF(16)

        label_widget = QLabel(f"{label}: ")
        label_widget.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        label_widget.setFont(font)
        layout.addWidget(label_widget)

        text.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        text.setFont(font)

        value_widget = text
        if image:
            value_container = QWidget()
            container_layout = QHBoxLayout()
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
            )

            image.setFixedSize(16, 16)
            container_layout.addWidget(image)
            container_layout.addWidget(text)
            value_container.setLayout(container_layout)
            value_widget = value_container

        layout.addWidget(value_widget)

        container.setLayout(layout)
        return container

    def connect(self):
        self.set_press_device_enabled(False)
        self.loader.start_animation()
        self.connect_button.setDisabled(True)
        self.restart_button.disable_button()

        virtual_port = get_virtual_port()
        if is_debug() and not virtual_port:
            QTimer.singleShot(0, lambda: self.handle_done_connect(True))
        else:
            if virtual_port: 
                self.address.setText(virtual_port)
            self.worker = Worker(
                self.thread,
                get_backend().connectToDevice,
                self.handle_exceptions,
                self.name.text(),
                self.address.text(),
            )
            self.worker.cancel_thread_on_timeout(15)
            self.worker.func_done.connect(self.handle_done_connect)
            self.thread.start()

    def handle_exceptions(self, e: Exception):
        handle_exception(e, None, None, self.error_message)
        self.reset_ui()

    def handle_done_connect(self, success: bool):
        if success:
            self.on_connect_success()
        else:
            self.on_connect_fail()

    def on_connect_success(self):
        self.loader.stop_animation()
        tray_icon = QSystemTrayIcon()
        tray_icon.showMessage(
            f"{self.name.text()} Connected",
            "Your device has now established a connection via Bluetooth.",
            QIcon(get_image_path("icon.svg")),
            3000,
        )
        self.switch_window(Dashboard(self.switch_window, self.name.text()))

    def on_connect_fail(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Connection Status")
        message_box.setText(f"{self.name.text()} Connection Failed")
        message_box.setInformativeText(self.error_message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        message_box.setIconPixmap(
            QIcon(get_image_path("icon.svg")).pixmap(QSize(64, 64))
        )
        message_box.exec()

        self.reset_ui()

    def reset_ui(self):
        self.loader.stop_animation()
        self.connect_button.setDisabled(False)
        self.restart_button.enable_button()
        self.set_press_device_enabled(True)

    def get_strength_from_rssi(self, rssi: int):
        if math.isinf(rssi):
            strength = "Unknown"
            return strength, None
        elif rssi < -95:
            strength = "No Signal"
            image = "none"
        elif rssi < -85:
            strength = "Poor"
            image = "poor"
        elif rssi < -75:
            strength = "Fair"
            image = "medium"
        elif rssi < -65:
            strength = "Good"
            image = "medium"
        else:
            strength = " Excellent"
            image = "excellent"

        return strength, f"signal_{image}.svg"
