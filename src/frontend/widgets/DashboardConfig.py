from typing import Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QFrame
from PySide6.QtGui import QFont

from frontend.widgets.DashboardButtonGroup import DashboardButtonGroup
from frontend.windows.ScrollableWindow import ScrollableWindow


class DashboardConfig(QWidget):
    def __init__(
        self, sensor_names: set[str], switch_window: Callable[[QWidget], None]
    ):
        super().__init__()

        self.sensor_scroll = ScrollableWindow(switch_window)

        self.sensor_title = QLabel("Detected Sensors")
        self.sensor_labels: list[QLabel] = []
        for sensor_name in sensor_names:
            self.sensor_labels.append(QLabel("\u25fc  " + sensor_name))

        self.horizontal_separator = QFrame()

        self.dashboard_button_group = DashboardButtonGroup(switch_window)

        self.init_ui()

    def init_ui(self):
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 25, 10, 0)

        self.sensor_scroll.main_layout.setContentsMargins(0, 0, 0, 0)

        sensor_layout = QVBoxLayout()
        sensor_layout.setContentsMargins(0, 0, 0, 0)

        sensor_title_font = QFont()
        sensor_title_font.setWeight(QFont.Weight.DemiBold)
        sensor_title_font.setPointSizeF(20)
        self.sensor_title.setFont(sensor_title_font)

        sensor_layout.addWidget(self.sensor_title)

        sensor_layout.addSpacing(5)

        sensor_name_font = QFont()
        sensor_name_font.setPointSizeF(16)

        for sensor_label in self.sensor_labels:
            sensor_label.setFont(sensor_name_font)
            sensor_layout.addWidget(sensor_label, 1)
        sensor_layout.addWidget(QWidget(), 1000)

        self.sensor_scroll.bind_scroll(sensor_layout)

        root_layout.addWidget(self.sensor_scroll)

        self.horizontal_separator.setFrameShape(QFrame.Shape.HLine)
        self.horizontal_separator.setFrameShadow(QFrame.Shadow.Sunken)
        root_layout.addWidget(self.horizontal_separator)

        root_layout.addWidget(self.dashboard_button_group)

        self.setLayout(root_layout)
