from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize

from frontend.widgets.DashboardStates.Streaming import Streaming


class StreamPrior(DashboardState):
    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.enable_button()
        self.dashboard_button_group.button_download.setEnabled(False)
        self.slot_to_disconnect = lambda: self.change_state(Streaming)
        self.dashboard_button_group.button_main.clicked.connect(self.slot_to_disconnect)

        self.dashboard_button_group.button_main.setEnabled(True)

        self.dashboard_button_group.button_main.setIconSize(QSize(18, 18))
        self.dashboard_button_group.button_main.setObjectName("play-button")

        return "START SESSION", "play.svg"
