from frontend.DebugData import get_debug_sensor_names
from frontend.config import get_backend, handle_exception, is_debug
from frontend.widgets.AddChartViews.AddChartView import AddChartView
from PySide6.QtWidgets import (
    QVBoxLayout,
    QCheckBox,
    QButtonGroup,
    QWidget,
    QLabel,
)
from PySide6.QtCore import Qt

from frontend.windows.ScrollableWindow import ScrollableWindow


class Multivariate(AddChartView):
    def __init__(self):
        super().__init__()

        self.title, self.title_input = self.create_text_input("Title")
        self.x_axis_label, self.x_axis_label_input = self.create_text_input(
            "X-Axis Label"
        )
        self.y_axis_label, self.y_axis_label_input = self.create_text_input(
            "Y-Axis Label"
        )

        self.select_sensors_container = ScrollableWindow(None)
        self.select_sensors_container.scroll_area.setObjectName("bordered")
        self.check_box_sensor_group = QButtonGroup()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.title)
        layout.addWidget(self.x_axis_label)
        layout.addWidget(self.y_axis_label)

        layout.addSpacing(20)

        select_sensor_root_container = self.init_select_sensor_ui()
        layout.addWidget(select_sensor_root_container)

        self.setLayout(layout)

    def init_select_sensor_ui(self):
        select_sensor_label = QLabel("Selected Sensors: ")
        select_sensor_label.setFont(self.get_form_font())

        self.select_sensors_container.setFixedSize(300, 200)
        self.select_sensors_container.main_layout.setContentsMargins(0, 0, 0, 0)
        select_sensor_layout = QVBoxLayout()
        select_sensor_layout.setSpacing(0)

        if is_debug():
            sensor_names = get_debug_sensor_names()
        else:
            sensor_names = get_backend().listSensorNames()
        for sensor in sensor_names:
            check_box = QCheckBox(sensor)
            select_sensor_layout.addWidget(check_box)
            self.check_box_sensor_group.addButton(check_box)
        select_sensor_layout.addWidget(QWidget(), 10000)

        self.check_box_sensor_group.setExclusive(False)
        self.select_sensors_container.bind_scroll(select_sensor_layout)

        return self.set_left_right_aligned_widgets(
            select_sensor_label, self.select_sensors_container
        )

    def on_submit_create(self):
        sensors_selected = []
        for button in self.check_box_sensor_group.buttons():
            if button.isChecked():
                sensors_selected.append(button.text())

        if len(sensors_selected) == 0:
            handle_exception(
                Exception("Sensors Not Selected"),
                None,
                False,
                "At least one sensor must be selected.",
            )
            return False, None
        
        id = get_backend().createChartObject(self.title_input.text(), self.x_axis_label_input.text(), self.y_axis_label_input.text(), sensors_selected, "line")

        return True, id
