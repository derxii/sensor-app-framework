from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize


class StreamEnd(DashboardState):
    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.enable_button()
        self.dashboard_button_group.button_download.setEnabled(True)

        self.dashboard_button_group.button_main.setIconSize(QSize(24, 24))
        self.dashboard_button_group.button_main.setObjectName("play-button")
        return "CLEAR SESSION", "clear.svg"

    def change_state(self):
        super().change_state()
        from frontend.widgets.DashboardStates.StreamPrior import StreamPrior

        self.change_dash_state(
            StreamPrior(self.change_dash_state, self.dashboard_button_group)
        )
