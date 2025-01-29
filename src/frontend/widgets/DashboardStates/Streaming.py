from typing import Callable
from frontend.widgets.DashboardButtonGroup import DashboardButtonGroup
from frontend.widgets.DashboardChart import DashboardChart
from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize

from frontend.widgets.DashboardStates.StreamEnd import StreamEnd


class Streaming(DashboardState):
    def __init__(
        self,
        change_dash_state: Callable[["DashboardState"], None],
        dashboard_button_group: DashboardButtonGroup,
        dashboard_chart: DashboardChart = None,
    ):
        super().__init__(change_dash_state, dashboard_button_group, dashboard_chart)
        self.dashboard_chart.can_create_delete(False)

    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.disable_button()
        self.dashboard_button_group.button_download.setEnabled(False)
        self.slot_to_disconnect = lambda: self.change_state(StreamEnd)
        self.dashboard_button_group.button_main.clicked.connect(self.slot_to_disconnect)

        self.dashboard_button_group.button_main.setIconSize(QSize(22, 22))
        self.dashboard_button_group.button_main.setObjectName("stop-button")
        return "STOP SESSION", "pause.svg"
