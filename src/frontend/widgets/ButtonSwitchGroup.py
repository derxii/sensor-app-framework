from typing import Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QFont

from frontend.config import dynamically_repaint_widget
from frontend.widgets.AddChartViews.AddChartView import AddChartView
from frontend.widgets.AddChartViews.Multivariate import Multivariate
from frontend.widgets.AddChartViews.Univariate import Univariate
from frontend.widgets.Button import Button


class ButtonSwitchGroup(QWidget):
    def __init__(
        self,
        initial_chart_view: AddChartView,
        switch_view: Callable[[AddChartView], None],
    ):
        super().__init__()
        self.switch_view = switch_view

        self.init_ui(initial_chart_view)

    def init_ui(self, initial_chart_view: AddChartView):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 10)
        button_layout.setSpacing(0)

        self.univariate_button = self.create_button_switch("Univariate", Univariate)
        button_layout.addSpacing(1)

        self.multivariate_button = self.create_button_switch(
            "Multivariate", Multivariate
        )

        button_layout.addWidget(self.univariate_button, 1)
        button_layout.addWidget(self.multivariate_button, 1)

        self.refresh_switch_button_ui(initial_chart_view)

        self.setLayout(button_layout)

    def create_button_switch(self, text: str, change_to_class: AddChartView):
        button = Button(text)
        button.clicked.connect(lambda: self.switch_view(change_to_class))
        button.setFixedHeight(50)
        button.setDefault(False)
        button.setAutoDefault(False)

        font = QFont()
        font.setWeight(QFont.Weight.DemiBold)
        font.setPointSizeF(16)
        button.add_text_font(font)
        return button

    def refresh_switch_button_ui(self, chart_view: AddChartView):
        selected_name = "switch-selected"
        selected_text_name = "white"
        not_selected_name = "switch-not-selected"

        self.univariate_button.alter_name(not_selected_name, not_selected_name)
        self.multivariate_button.alter_name(not_selected_name, not_selected_name)

        if isinstance(chart_view, Univariate):
            self.univariate_button.alter_name(selected_name, selected_text_name)
        else:
            self.multivariate_button.alter_name(selected_name, selected_text_name)

        dynamically_repaint_widget(
            self.univariate_button,
            self.univariate_button.button_label,
            self.multivariate_button,
            self.multivariate_button.button_label,
        )
