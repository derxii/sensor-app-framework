from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from frontend.config import get_backend
from frontend.widgets.Button import Button
from frontend.widgets.DraggableResizable import DraggableResizable
from frontend.windows.AddChart import AddChart

if TYPE_CHECKING:
    from frontend.widgets.DashboardStates.DashboardState import DashboardState


class DashboardChart(QWidget):
    def __init__(
        self,
        get_dashboard_state: Callable[[], "DashboardState"],
        device_name: str,
        switch_window: Callable[[QWidget], None],
    ):
        super().__init__()
        self.get_dashboard_state = get_dashboard_state
        self.switch_window = switch_window

        self.title = QLabel(device_name)
        self.chart_area = QWidget()

        self.no_chart_text = QLabel(
            "At least one chart must be added before streaming data"
        )
        self.add_chart_button = Button("+ Add Chart", None, "add-chart", "blue")
        self.add_chart_button.clicked.connect(self.open_create_chart_form)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)

        title_font = QFont()
        title_font.setWeight(QFont.Weight.DemiBold)
        title_font.setPointSizeF(32)
        self.title.setFont(title_font)

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        layout.addWidget(self.title, 1)
        layout.addSpacing(5)

        self.init_chart_ui()
        layout.addWidget(self.chart_area, 1000)
        layout.addSpacing(5)

        font_button = QFont()
        font_button.setWeight(QFont.Weight.DemiBold)
        font_button.setPointSizeF(18)
        self.add_chart_button.add_text_font(font_button)

        self.add_chart_button.setFixedHeight(40)
        layout.addWidget(self.add_chart_button, 1)

        self.setLayout(layout)

    def init_chart_ui(self):
        chart_layout = QVBoxLayout()

        no_chart_font = QFont()
        no_chart_font.setItalic(True)
        no_chart_font.setPointSizeF(18)
        self.no_chart_text.setFont(no_chart_font)
        chart_layout.addWidget(self.no_chart_text, 0, Qt.AlignmentFlag.AlignCenter)

        self.chart_area.setLayout(chart_layout)

        for chart in get_backend().getChartObjects():
            self.generate_chart(chart.getId())
        self.get_dashboard_state().handle_change_chart_amount(self.no_chart_text)

    def generate_chart(self, existing_id: str):
        new_chart = DraggableResizable(self, self.chart_area, existing_id)
        new_chart.show()

    def can_create_delete(self, value: bool):
        self.add_chart_button.setEnabled(value)
        self.chart_area.setEnabled(value)

    def open_create_chart_form(self):
        add_chart_form = AddChart(self.window().geometry(), self.window().minimumSize())
        add_success = add_chart_form.exec()
        if add_success:
            self.get_dashboard_state().handle_change_chart_amount(self.no_chart_text)
            QTimer.singleShot(100, lambda: self.generate_chart(add_chart_form.created_chart_id))