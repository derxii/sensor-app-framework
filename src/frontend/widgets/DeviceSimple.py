from typing import Callable
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
)
from PySide6.QtGui import QFont, Qt, QMouseEvent

from frontend.config import dynamically_repaint_widget, enable_custom_styling
from frontend.widgets.DeviceDetailed import DeviceDetailed


class DeviceSimple(QWidget):
    def __init__(
        self,
        name: str,
        address: str,
        rssi: int,
        set_current_selected_device_index: Callable[[int], None],
        index: int,
    ):
        super().__init__()
        self.name = QLabel(name)
        self.address = QLabel(address)
        self.separator = QFrame()

        self.rssi = rssi
        self.index = index
        self.set_current_selected_device_index = set_current_selected_device_index

        self.init_ui()

    def init_ui(self):
        root_layout = QHBoxLayout()
        root_layout.addSpacing(10)
        container = QWidget()

        container_layout = QVBoxLayout()
        container_layout.addSpacing(5)

        name_font = QFont()
        name_font.setPointSizeF(18)
        name_font.setWeight(QFont.Weight.Medium)
        self.name.setFont(name_font)

        self.name.setWordWrap(True)
        self.name.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        container_layout.addWidget(self.name)

        address_font = QFont()
        address_font.setPointSizeF(11)
        address_font.setItalic(True)
        self.address.setFont(address_font)

        container_layout.addWidget(self.address)

        size_policy = self.separator.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.separator.setSizePolicy(size_policy)

        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(self.separator)

        root_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setContentsMargins(0, 0, 10, 0)
        container.setLayout(container_layout)

        root_layout.addWidget(container)
        self.setLayout(root_layout)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.select()
        super().mousePressEvent(event)

    def select(self):
        if self.set_current_selected_device_index(self.index):
            self.setObjectName("selected")
            self.name.setObjectName("white")
            self.address.setObjectName("white")
            self.separator.setHidden(True)
            dynamically_repaint_widget(self, self.name, self.address)

    def reset_select(self):
        self.setObjectName("")
        self.name.setObjectName("")
        self.address.setObjectName("")
        self.separator.setHidden(False)
        dynamically_repaint_widget(self, self.name, self.address)

    def paintEvent(self, _):
        enable_custom_styling(self)

    def generate_detailed_view(self, switch_window: Callable[[QWidget], None]):
        return DeviceDetailed(
            self.name.text(),
            self.address.text(),
            self.rssi,
            switch_window,
            self.parentWidget().setEnabled,
        )
