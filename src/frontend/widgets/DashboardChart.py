from typing import TYPE_CHECKING, Callable
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QGridLayout, QMainWindow
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from backend.LivePlots.LiveDataPlot import LiveDataPlot
from backend.StaticPlots.StaticDataPlot import StaticDataPlot
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

        self.chart_area = QMainWindow()
        central_widget = QWidget()
        self.chart_area.setCentralWidget(central_widget)
        self.chart_area_layout = QGridLayout()
        central_widget.setLayout(self.chart_area_layout)
        self.no_chart_text = QLabel(
            "At least one chart must be added before streaming data."
        )

        self.add_chart_button = Button("+ Add Chart", None, "add-chart", "blue")
        self.add_chart_button.clicked.connect(self.open_create_chart_form)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)

        title_font = QFont()
        title_font.setWeight(QFont.Weight.DemiBold)
        title_font.setPointSizeF(32)
        self.title.setFont(title_font)

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.layout.addWidget(self.title, 1)
        self.layout.addSpacing(5)

        self.chart_area.setObjectName("dock-area")

        no_chart_font = QFont()
        no_chart_font.setItalic(True)
        no_chart_font.setPointSizeF(18)
        self.no_chart_text.setFont(no_chart_font)
        self.layout.addWidget(self.no_chart_text, 1000, Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(5)

        font_button = QFont()
        font_button.setWeight(QFont.Weight.DemiBold)
        font_button.setPointSizeF(18)
        self.add_chart_button.add_text_font(font_button)

        self.add_chart_button.setFixedHeight(40)
        self.layout.addWidget(self.add_chart_button, 1)

        self.setLayout(self.layout)

    def refresh_chart_layout(self):
        if hasattr(self, "LiveWindow"):
            self.LiveWindow.clearPlots()
            self.LiveWindow.__del__()
            self.chart_area.setParent(None)
            self.chart_area = QMainWindow()
            central_widget = QWidget()
            self.chart_area.setCentralWidget(central_widget)
            self.chart_area_layout = QGridLayout()
            central_widget.setLayout(self.chart_area_layout)
            self.layout.insertWidget(
                2, self.chart_area, 1000
            )
        print(len(get_backend().chartObjects))
        self.LiveWindow = LiveDataPlot(get_backend(), self.chart_area, self.chart_area_layout)
        return
    def refresh_static_plots(self):
        self.StaticWindow = StaticDataPlot(get_backend(), self.chart_area)
        return

    def can_create_delete(self, value: bool):
        self.add_chart_button.setEnabled(value)
        for chart in self.chart_area.findChildren(DraggableResizable):
            chart.set_enabled_closing(value)

    def open_create_chart_form(self):
        add_chart_form = AddChart(self.window().geometry(), self.window().minimumSize())
        add_success = add_chart_form.exec()
        if add_success:
            self.get_dashboard_state().handle_change_chart_amount(self)
            QTimer.singleShot(
                100, self.refresh_chart_layout
            )

    def hideControlsDock(self):
        if hasattr(self, "LiveWindow"):
            self.LiveWindow.hideControls()

    def setPauseLivePlot(self, val):
        if hasattr(self, "LiveWindow"):
            self.LiveWindow.set_pause(val)

