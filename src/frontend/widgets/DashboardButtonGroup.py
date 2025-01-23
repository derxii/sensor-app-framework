from typing import Callable, Literal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from frontend.widgets.Button import Button
from frontend.widgets.ResetButton import ResetButton


class DashboardButtonGroup(QWidget):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__()

        self.status: Literal["stream-prior", "streaming", "stream-end"] = "stream-prior"

        self.button_restart = ResetButton(False, switch_window)
        self.button_download = Button("DOWNLOAD DATA")
        self.button_main = Button("")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button_restart)
        layout.addWidget(self.button_download)
        layout.addWidget(self.button_main)

        self.refresh_ui()
        self.setLayout(layout)

    def refresh_ui(self):
        if self.status == "stream-prior":
            self.button_restart.setEnabled(True)
            self.button_download.setEnabled(False)
            self.button_main.change_text("START SESSION")

        elif self.status == "streaming":
            self.button_restart.setEnabled(False)
            self.button_download.setEnabled(False)
            self.button_main.change_text("STOP SESSION")
        else:
            self.button_restart.setEnabled(True)
            self.button_download.setEnabled(True)
            self.button_main.change_text("CLEAR SESSION")
