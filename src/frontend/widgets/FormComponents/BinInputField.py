from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt

from frontend.config import get_image_path, handle_exception
from frontend.widgets.FormComponents.BinInput import BinInput
from frontend.widgets.FormComponents.FormUtils import (
    get_form_font,
    set_left_right_aligned_widgets,
)


class BinInputField(QWidget):
    def __init__(self, label: str = "Data Bins: "):
        super().__init__()

        self.bin_label = QLabel(label)
        self.bin_tooltip = QLabel("")

        self.bin_input = BinInput()

        self.init_ui()

    def init_ui(self):
        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)

        left_container = QWidget()
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.bin_label.setFont(get_form_font())
        left_layout.addWidget(self.bin_label)

        image = QIcon(get_image_path("tooltip.svg")).pixmap(QSize(18, 18))
        self.bin_tooltip.setObjectName("tooltip")
        self.bin_tooltip.setPixmap(image)
        self.bin_tooltip.setToolTip(
            "Start is inclusive, while end is exclusive [Start, End)"
        )
        left_layout.addWidget(self.bin_tooltip)

        left_container.setLayout(left_layout)

        root_container = set_left_right_aligned_widgets(
            left_container, self.bin_input, 1, 1, Qt.AlignmentFlag.AlignTop
        )
        root_layout.addWidget(root_container)
        self.setLayout(root_layout)

    def get_bin_values(self):
        return self.bin_input.bin_value_container.get_bins()

    def set_no_bin_exception(self):
        handle_exception(
            Exception("Not Enough Bins"), None, None, "Please add at least one bin."
        )