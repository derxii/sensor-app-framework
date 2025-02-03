from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize


class StreamEnd(DashboardState):
    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.enable_button()
        self.dashboard_button_group.button_download.setEnabled(True)

        from frontend.widgets.DashboardStates.StreamPrior import StreamPrior

        self.slot_to_disconnect = lambda: self.change_state(StreamPrior)
        self.dashboard_button_group.button_main.clicked.connect(self.slot_to_disconnect)

        self.dashboard_button_group.button_main.setIconSize(QSize(24, 24))
        self.dashboard_button_group.button_main.setObjectName("play-button")
        return "CLEAR SESSION", "clear.svg"

    def change_state(self, dashboard_state: DashboardState):
        self.dashboard_chart.can_create_delete(True)
        super().change_state(dashboard_state)
