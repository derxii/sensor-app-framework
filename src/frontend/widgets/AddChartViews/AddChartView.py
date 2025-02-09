from abc import abstractmethod
from typing import Union
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QCheckBox,
    QButtonGroup,
)
from PySide6.QtGui import Qt

from frontend.DebugData import get_debug_sensor_names
from frontend.config import get_backend, is_debug
from frontend.widgets.AddChartViews.TypeSelector import TypeSelector
from frontend.widgets.ChartHandlers.LineChartHandler import LineChartHandler
from frontend.widgets.ChartHandlers.ChartHandler import ChartHandler
from frontend.widgets.FormComponents.FormUtils import (
    create_text_input,
    get_form_font,
    set_left_right_aligned_widgets,
)
from frontend.windows.ScrollableWindow import ScrollableWindow


class AddChartView(QWidget):
    def __init__(self, text_chart_handler_mapping: dict[str, ChartHandler]):
        super().__init__()

        self.chart_handler: ChartHandler = LineChartHandler()
        self.type_selector_container = TypeSelector.create_type_selector_form_container(
            text_chart_handler_mapping, self.switch_chart_handler
        )
        self.select_sensors_container = ScrollableWindow(None)
        self.select_sensors_container.scroll_area.setObjectName("bordered")
        self.select_sensor_button_group = QButtonGroup()

        self.title, self.title_input = create_text_input("Title")
        self.custom_fields_widget: Union[None, QWidget] = None

    def init_ui(self, is_radio: bool):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addSpacing(10)

        layout.addWidget(self.type_selector_container)
        select_sensor_root_container = self.init_select_sensor_ui(is_radio)
        layout.addWidget(select_sensor_root_container)
        layout.addSpacing(10)

        layout.addWidget(self.title)
        self.custom_fields_widget = self.chart_handler.get_custom_fields_container()
        layout.addWidget(self.custom_fields_widget)

        self.setLayout(layout)

    def init_select_sensor_ui(self, is_radio: bool):
        select_sensor_label = QLabel("Selected Sensors: ")
        select_sensor_label.setFont(get_form_font())

        self.select_sensors_container.setFixedSize(300, 200)
        self.select_sensors_container.main_layout.setContentsMargins(0, 0, 0, 0)
        select_sensor_layout = QVBoxLayout()
        select_sensor_layout.setSpacing(0)

        if is_debug():
            sensor_names = get_debug_sensor_names()
        else:
            sensor_names = get_backend().listSensorNames()

        for sensor in sensor_names:
            if is_radio:
                selection = QRadioButton(sensor)
            else:
                selection = QCheckBox(sensor)
            select_sensor_layout.addWidget(selection)
            self.select_sensor_button_group.addButton(selection)

        select_sensor_layout.addWidget(QWidget(), 10000)

        self.select_sensor_button_group.setExclusive(True if is_radio else False)
        self.select_sensors_container.bind_scroll(select_sensor_layout)

        return set_left_right_aligned_widgets(
            select_sensor_label,
            self.select_sensors_container,
            1,
            1,
            Qt.AlignmentFlag.AlignTop,
        )

    def get_sensors_selected(self):
        sensors_selected = []
        for button in self.select_sensor_button_group.buttons():
            if button.isChecked():
                sensors_selected.append(button.text())
        return sensors_selected

    def switch_chart_handler(self, new_chart_handler: ChartHandler):
        self.custom_fields_widget.setParent(None)
        self.custom_fields_widget.deleteLater()
        self.chart_handler = new_chart_handler

        self.custom_fields_widget = self.chart_handler.get_custom_fields_container()
        self.layout().addWidget(self.custom_fields_widget)

    @abstractmethod
    def on_submit_create(self) -> tuple[bool, Union[int, None]]:
        pass
