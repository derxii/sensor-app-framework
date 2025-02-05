from typing import Callable
from frontend.config import handle_exception
from frontend.thread.Worker import Worker
from frontend.widgets.DashboardButtonGroup import DashboardButtonGroup
from frontend.widgets.DashboardChart import DashboardChart
from frontend.widgets.DashboardStates.DashboardState import DashboardState
from PySide6.QtCore import QSize, QThread

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
        self.session_thread = QThread()
        self.setup_backend_worker()

    def setup_backend_worker(self):
        self.worker = Worker(
            self.session_thread,
            self.stream,
            lambda e: handle_exception(e, None, True),
        )
        self.session_thread.start()

    async def stream(self):
        import asyncio

        while True:
            await asyncio.sleep(0.1)

    def done_session(self):
        self.worker.stop()
        self.session_thread.wait()
        self.change_state(StreamEnd)

    def set_new_button_info(self) -> tuple[str, str]:
        self.dashboard_button_group.button_restart.disable_button()
        self.dashboard_button_group.button_download.setEnabled(False)
        self.slot_to_disconnect = self.done_session
        self.dashboard_button_group.button_main.clicked.connect(self.slot_to_disconnect)

        self.dashboard_button_group.button_main.setIconSize(QSize(22, 22))
        self.dashboard_button_group.button_main.setObjectName("stop-button")
        return "STOP SESSION", "pause.svg"
