from typing import Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy, QHBoxLayout, QPushButton, QSystemTrayIcon, QMessageBox
from PySide6.QtGui import QFont, Qt, QIcon
from PySide6.QtCore import QSize, QTimer

from frontend.config import dynamically_repaint_widget, get_image_path
from frontend.widgets.Loader import Loader
from frontend.widgets.ResetButton import ResetButton
from frontend.windows.ScrollableWindow import ScrollableWindow

class DeviceDetailed(ScrollableWindow):
    def __init__(self, 
                 name: str, 
                 address: str, 
                 rssi: int,
                 switch_window: Callable[[QWidget], None]
                ):

        super().__init__(switch_window)
        self.name = QLabel(name)
        self.address = QLabel(address)
        self.rssi = QLabel(f"{rssi}dBm")

        if rssi < -95:
            strength = "No Signal"
        elif rssi < -85:
            strength = "Poor"
        elif rssi < -75:
            strength = "Fair"
        elif rssi < -65:
            strength = "Good"
        else:
            strength = "Excellent"

        self.signal_strength = QLabel(strength)

        self.loader = Loader(200)

        self.restart_button = ResetButton(True, self.switch_window)
        self.connect_button = QPushButton("Connect")

        self.connect_button.clicked.connect(self.connect)

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

        root_layout.addSpacing(10)

        root_layout.addWidget(self.create_left_right_aligned_text(self.address, "Address"))
        root_layout.addWidget(self.create_left_right_aligned_text(self.rssi, "RSSI"))
        root_layout.addWidget(self.create_left_right_aligned_text(self.signal_strength, "Signal Strength"))

        root_layout.addWidget(self.loader, 3)

        bottom_container = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.connect_button.setObjectName("connect-button")
        connect_font = QFont()
        connect_font.setWeight(QFont.Weight.DemiBold)
        self.connect_button.setFont(connect_font)
        self.connect_button.setMinimumWidth(150)

        bottom_layout.addWidget(self.restart_button)
        bottom_layout.addWidget(self.connect_button)

        bottom_container.setLayout(bottom_layout)

        root_layout.addWidget(bottom_container, 1)

        self.bind_scroll(root_layout)

    def create_left_right_aligned_text(self, text: QLabel, label: str):
        container = QWidget()
        container.setMaximumHeight(40)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout()

        font = QFont()
        font.setPointSizeF(16)

        label_widget = QLabel(f"{label}: ")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_widget.setFont(font)
        layout.addWidget(label_widget)

        text.setAlignment(Qt.AlignmentFlag.AlignRight)
        text.setFont(font)
        layout.addWidget(text)

        container.setLayout(layout)
        return container
    
    def connect(self):
        self.loader.start_animation()
        self.connect_button.setDisabled(True)
        self.restart_button.setDisabled(True)
        self.connect_button.setObjectName("disabled")
        self.restart_button.disable_button()
        dynamically_repaint_widget(self.connect_button)

        QTimer.singleShot(2000, self.on_connect_fail)

    
    def on_connect_success(self):
        self.loader.stop_animation()
        tray_icon = QSystemTrayIcon()
        tray_icon.showMessage(
            f"{self.name.text()} Connected", 
            "Your device has now established a connection via Bluetooth.", 
            QIcon(get_image_path("icon.svg")), 
            3000
        )

    def on_connect_fail(self):
        self.loader.stop_animation()

        message_box = QMessageBox()
        message_box.setWindowTitle("Connection Status")
        message_box.setText(f"{self.name.text()} Connection Failed")
        message_box.setInformativeText("Please try connecting again or use " + 
                                       "another Bluetooth device.")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        message_box.setIconPixmap(QIcon(get_image_path("icon.svg")).pixmap(QSize(64, 64)))
        message_box.exec()

        self.connect_button.setDisabled(False)
        self.restart_button.setDisabled(False)
        self.connect_button.setObjectName("connect-button")
        self.restart_button.enable_button()
        dynamically_repaint_widget(self.connect_button)