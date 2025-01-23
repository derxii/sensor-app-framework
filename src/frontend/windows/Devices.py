from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PySide6.QtGui import Qt
from typing import Callable

from frontend.widgets.DeviceSimple import DeviceSimple
from frontend.widgets.NoDeviceHint import NoDeviceHint
from frontend.windows.ScrollableWindow import ScrollableWindow
from frontend.config import default_width

left_container_width = 300


class Devices(ScrollableWindow):
    def __init__(
        self,
        switch_window: Callable[[QWidget], None],
        name_address_rssi_list: list[tuple[str, str, int]],
    ):
        super().__init__(switch_window)

        self.selected_device_index = None

        self.device_simple_view_list: list[DeviceSimple] = []
        for i, (name, address, rssi) in enumerate(name_address_rssi_list):
            self.device_simple_view_list.append(
                DeviceSimple(
                    name, address, rssi, self.set_current_selected_device_index, i
                )
            )

        self.left_container_scroll = QScrollArea()
        self.left_container_scroll.setWidgetResizable(True)

        self.left_container_simple = QWidget()
        self.left_container_scroll.setWidget(self.left_container_simple)

        self.separator = QFrame()

        self.right_container_detailed = QWidget()
        self.right_container_layout = QVBoxLayout()

        self.init_ui(left_container_width)

    def init_ui(self, left_container_width: int):
        layout = QHBoxLayout()

        self.left_container_scroll.setFixedWidth(left_container_width)

        left_container_layout = QVBoxLayout()
        left_container_layout.setSpacing(0)
        left_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.left_container_simple.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
        )

        for device_simple in self.device_simple_view_list:
            device_simple.setMinimumHeight(30)
            device_simple.setSizePolicy(
                QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
            )
            left_container_layout.addWidget(device_simple, 1)
        left_container_layout.addWidget(QWidget(), 1000)

        self.left_container_simple.setObjectName("scrollable-window")
        self.left_container_simple.setLayout(left_container_layout)

        layout.addWidget(self.left_container_scroll)

        self.left_container_scroll.setContentsMargins(0, 0, 0, 0)
        left_container_layout.setContentsMargins(0, 0, 0, 0)
        self.left_container_simple.setContentsMargins(0, 0, 0, 0)

        self.separator.setFrameShape(QFrame.Shape.VLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.separator)

        self.right_container_detailed.setMinimumWidth(
            default_width - left_container_width - 200
        )
        self.right_container_detailed.setLayout(self.right_container_layout)

        self.right_container_layout.addWidget(NoDeviceHint(self.switch_window))
        layout.addWidget(self.right_container_detailed)

        layout.setContentsMargins(5, 5, 5, 5)
        self.bind_scroll(layout)

    def set_current_selected_device_index(self, device_index: int):
        if self.selected_device_index != device_index:
            if self.selected_device_index is not None:
                removed_device = self.device_simple_view_list[
                    self.selected_device_index
                ]
                removed_device.reset_select()
            self.selected_device_index = device_index

            selected_device = self.device_simple_view_list[device_index]

            self.right_container_layout.itemAt(0).widget().setParent(None)
            self.right_container_layout.addWidget(
                selected_device.generate_detailed_view(self.switch_window)
            )
            return True

        return False
