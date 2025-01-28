from PySide6.QtWidgets import QSizeGrip, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from frontend.config import enable_custom_styling, get_backend, get_image_path
from frontend.widgets.DraggableTopBar import DraggableTopBar

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.widgets.DashboardChart import DashboardChart


class DraggableResizable(QWidget):
    def __init__(self, parent: "DashboardChart", container: QWidget, chart_id: str):
        super().__init__(container)
        self.setWindowFlag(Qt.WindowType.SubWindow)
        self.parent = parent
        self.chart_id = chart_id

        self.top_bar = DraggableTopBar(self)
        self.contents = QWidget()
        self.bottom_bar = QWidget()
        self.grip = QSizeGrip(self)

        self.setGeometry(0, 0, 300, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.top_bar)
        layout.addWidget(self.contents)
        layout.addWidget(self.bottom_bar)

        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 2, 2)
        bottom_layout.addWidget(
            self.grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        self.grip.setFixedSize(8, 8)
        self.grip.setStyleSheet(
            """QSizeGrip {
            image: url("""
            + get_image_path("gripper.svg")
            + """);
            width: 8px;
            height: 8px;
        }"""
        )

        self.bottom_bar.setLayout(bottom_layout)
        self.setLayout(layout)

    def paintEvent(self, _):
        enable_custom_styling(self)

    def destroy(self):
        get_backend().deleteChart(self.chart_id)

        self.parent.dashboard_state.handle_change_chart_amount(
            self.parent.no_chart_text
        )
        self.setParent(None)
