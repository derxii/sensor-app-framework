from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize


class NoChart(DashboardState):
    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.enable_button()
        self.dashboard_button_group.button_download.setEnabled(False)

        self.dashboard_button_group.button_main.setEnabled(False)

        self.dashboard_button_group.button_main.setIconSize(QSize(18, 18))
        self.dashboard_button_group.button_main.setObjectName("play-button")

        return "START SESSION", "play.svg"

    def change_state(self, dashboard_state: "DashboardState"):
        self.change_dash_state(
            dashboard_state(self.change_dash_state, self.dashboard_button_group)
        )
