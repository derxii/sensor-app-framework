from abc import ABC, abstractmethod
from typing import Callable

from frontend.config import dynamically_repaint_widget, get_image_path
from frontend.widgets.DashboardButtonGroup import DashboardButtonGroup


class DashboardState(ABC):
    def __init__(
        self,
        change_dash_state: Callable[["DashboardState"], None],
        dashboard_button_group: DashboardButtonGroup,
    ):
        self.dashboard_button_group = dashboard_button_group
        self.change_dash_state = change_dash_state
        self.slot_to_disconnect = None

        self.set_button_state()

    def set_button_state(self):
        main_button_text, icon_location = self.set_new_button_info()

        self.dashboard_button_group.button_main.change_text(main_button_text)
        self.dashboard_button_group.button_main.set_icon(get_image_path(icon_location))

        dynamically_repaint_widget(self.dashboard_button_group.button_main)

    @abstractmethod
    def set_new_button_info(
        self, button_group: DashboardButtonGroup
    ) -> tuple[str, str]:
        pass

    def change_state(self, dashboard_state: "DashboardState"):
        self.dashboard_button_group.button_main.clicked.disconnect(
            self.slot_to_disconnect
        )
        self.change_dash_state(
            dashboard_state(self.change_dash_state, self.dashboard_button_group)
        )
