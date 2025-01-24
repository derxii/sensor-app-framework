from PySide6.QtWidgets import QHBoxLayout, QWidget, QFrame
from typing import Callable

from frontend.DebugData import get_debug_sensor_names
from frontend.config import get_backend, is_debug
from frontend.widgets.DashboardConfig import DashboardConfig
from frontend.widgets.DashboardStates.DashboardState import DashboardState
from frontend.widgets.DashboardStates.StreamPrior import StreamPrior
from frontend.windows.ScrollableWindow import ScrollableWindow


class Dashboard(ScrollableWindow):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)

        if is_debug():
            self.sensor_names: set[str] = get_debug_sensor_names()
        else:
            self.sensor_names: set[str] = get_backend().listSensorNames()

        self.left_container = DashboardConfig(self.sensor_names, switch_window)
        self.vertical_separator = QFrame()
        self.right_container = QWidget()

        self.dashboard_state: DashboardState = StreamPrior(
            self.change_state,
            self.left_container.dashboard_button_group,
        )
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.left_container.setFixedWidth(235)
        layout.addWidget(self.left_container)

        self.vertical_separator.setFrameShape(QFrame.Shape.VLine)
        self.vertical_separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(self.vertical_separator)

        layout.addWidget(self.right_container, 1)

        self.bind_scroll(layout)

    def change_state(self, new_state: DashboardState):
        self.dashboard_state = new_state
