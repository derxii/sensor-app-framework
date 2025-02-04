from typing import Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFileDialog, QSystemTrayIcon
from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QIcon

from frontend.config import get_image_path
from frontend.widgets.Button import Button
from frontend.widgets.ResetButton import ResetButton


class DashboardButtonGroup(QWidget):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__()

        self.button_restart = ResetButton(False, switch_window)
        self.button_download = Button(
            "DOWNLOAD DATA", get_image_path("download.svg"), "download-button", "green"
        )
        self.button_main = Button("", None, "", "white")
        self.button_main_slot = None

        self.button_download.clicked.connect(self.download_data)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_restart)

        font = QFont()
        font.setWeight(QFont.Weight.DemiBold)

        self.button_download.add_text_font(font)
        self.button_download.setIconSize(QSize(24, 24))
        self.button_download.setFixedHeight(36)
        layout.addWidget(self.button_download)

        self.button_main.add_text_font(font)
        self.button_main.setFixedHeight(39)
        layout.addWidget(self.button_main)

        self.setLayout(layout)

    def download_data(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Data as a .csv File", "data.csv"
        )

        tray_icon = QSystemTrayIcon()
        tray_icon.showMessage(
            "Data Downloaded",
            "Your data has been saved to " + save_path,
            QIcon(get_image_path("icon.svg")),
            3000,
        )
