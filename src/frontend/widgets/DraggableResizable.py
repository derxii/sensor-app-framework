from PySide6.QtWidgets import QWidget, QDockWidget, QHBoxLayout, QLabel, QMainWindow


from typing import TYPE_CHECKING

from frontend.config import dynamically_repaint_widget, get_backend

if TYPE_CHECKING:
    from frontend.widgets.DashboardChart import DashboardChart


class DraggableResizable(QDockWidget):
    def __init__(self, parent: "DashboardChart", container: QMainWindow, chart_id: int):
        super().__init__(container)
        self.parent = parent
        self.chart_id = chart_id

        self.widget = QWidget()
        self.topLevelChanged.connect(self.on_change_level)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.widget.setObjectName("chart-container-docked")

        layout.addWidget(QLabel("hello"), 100)

        self.widget.setLayout(layout)
        self.setWidget(self.widget)
        self.set_enabled_closing(True)

    def set_enabled_closing(self, enable: bool):
        if enable:
            self.setFeatures(
                QDockWidget.DockWidgetFeature.DockWidgetFloatable
                | QDockWidget.DockWidgetFeature.DockWidgetMovable
                | QDockWidget.DockWidgetFeature.DockWidgetClosable
            )
        else:
            self.setFeatures(
                QDockWidget.DockWidgetFeature.DockWidgetFloatable
                | QDockWidget.DockWidgetFeature.DockWidgetMovable
            )

    def closeEvent(self, _):
        get_backend().deleteChart(self.chart_id)

        self.parent.get_dashboard_state().handle_change_chart_amount(self.parent)
        self.setParent(None)
        self.deleteLater()

    def on_change_level(self, is_floating: bool):
        if is_floating:
            self.widget.setObjectName("")
        else:
            self.widget.setObjectName("chart-container-docked")

        dynamically_repaint_widget(self.widget)
