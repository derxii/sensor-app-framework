from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize

from frontend.widgets.DashboardStates.StreamEnd import StreamEnd


class Streaming(DashboardState):
    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.disable_button()
        self.dashboard_button_group.button_download.setEnabled(False)

        self.dashboard_button_group.button_main.setIconSize(QSize(22, 22))
        self.dashboard_button_group.button_main.setObjectName("stop-button")
        return "STOP SESSION", "pause.svg"

    def change_state(self):
        super().change_state()
        self.change_dash_state(
            StreamEnd(self.change_dash_state, self.dashboard_button_group)
        )
