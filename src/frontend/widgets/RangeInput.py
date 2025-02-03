from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QDoubleSpinBox

from frontend.config import handle_exception
from frontend.widgets.FormUtils import get_form_font, set_left_right_aligned_widgets


class RangeInput(QWidget):
    def create_range_input(label: str = "Min-Max Range"):
        font = get_form_font()

        label_widget = QLabel(f"{label}: ")
        label_widget.setFont(font)

        range_input = RangeInput()

        container = set_left_right_aligned_widgets(label_widget, range_input, 1, 1)

        return container, range_input

    def __init__(self):
        super().__init__()

        self.start_input = QDoubleSpinBox()
        self.separator_dash = QFrame()
        self.end_input = QDoubleSpinBox()

        self.start_input.setRange(-1e200, 1e200)
        self.end_input.setRange(-1e200, 1e200)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.start_input.setMinimumWidth(50)
        self.start_input.setFont(get_form_font())
        layout.addWidget(self.start_input, 3)

        self.separator_dash.setFrameShape(QFrame.Shape.HLine)
        self.separator_dash.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(self.separator_dash, 1)

        self.end_input.setMinimumWidth(50)
        self.end_input.setFont(get_form_font())
        layout.addWidget(self.end_input, 3)

        self.setLayout(layout)

    def get_bin_value(self):
        lower_value = self.start_input.value()
        upper_value = self.end_input.value()

        root_exception = Exception("Bad Range")

        if lower_value >= upper_value:
            handle_exception(
                root_exception,
                None,
                None,
                "End binned value must be strictly greater than the start binned value.",
            )
            return

        return lower_value, upper_value
