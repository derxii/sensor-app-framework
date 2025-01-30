from PySide6.QtWidgets import QVBoxLayout, QDialog
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFont

from frontend.widgets.AddChartViews.AddChartView import AddChartView
from frontend.widgets.AddChartViews.Multivariate import Multivariate
from frontend.widgets.Button import Button
from frontend.windows.ScrollableWindow import ScrollableWindow


class AddChart(QDialog):
    def __init__(self, previous_window_geometry: QRect, minimum_size: QSize):
        super().__init__()

        self.created_chart_id = None

        self.container = ScrollableWindow(None)
        self.chart_view: AddChartView = Multivariate()
        self.create_chart_button = Button("+ Create", None, "create-chart", "white")
        self.create_chart_button.clicked.connect(self.try_submit)

        self.init_ui(previous_window_geometry, minimum_size)

    def init_ui(self, previous_window_geometry: QRect, minimum_size: QSize):
        self.setGeometry(previous_window_geometry)
        self.setWindowTitle("Add Chart")
        self.setMinimumSize(minimum_size)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        self.container.main_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.container)

        self.view_layout = QVBoxLayout()
        self.view_layout.setContentsMargins(0, 0, 40, 0)
        self.view_layout.addWidget(self.chart_view)

        button_font = QFont()
        button_font.setWeight(QFont.Weight.DemiBold)
        button_font.setPointSizeF(20)

        self.create_chart_button.add_text_font(button_font)
        self.create_chart_button.setFixedSize(150, 40)
        self.view_layout.addWidget(
            self.create_chart_button, 0, Qt.AlignmentFlag.AlignRight
        )

        self.view_layout.addSpacing(40)

        self.container.bind_scroll(self.view_layout)
        self.setLayout(root_layout)

    def change_add_chart_view(self, new_view: AddChartView):
        self.view_layout.children[0].setParent(None)
        self.chart_view = new_view
        self.view_layout.addChildWidget(self.chart_view)

    def try_submit(self):
        success, chart_id = self.chart_view.on_submit_create()
        self.created_chart_id = chart_id
        if success:
            super().accept()
