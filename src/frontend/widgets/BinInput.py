from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtGui import Qt

from frontend.config import get_image_path
from frontend.widgets.BinAddedContainer import BinAddedContainer
from frontend.widgets.Button import Button
from frontend.widgets.RangeInput import RangeInput


class BinInput(QWidget):
    def __init__(self):
        super().__init__()

        self.range_input = RangeInput()
        self.add_range_button = Button("", get_image_path("add.svg"), "bin")

        self.bin_value_container = BinAddedContainer()

        self.add_range_button.clicked.connect(self.handle_add_bin)

        self.init_ui()

    def init_ui(self):
        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        root_layout.setContentsMargins(0, 0, 0, 0)

        top_container = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)

        top_layout.addWidget(self.range_input)
        top_layout.addWidget(self.add_range_button, 0, Qt.AlignmentFlag.AlignHCenter)

        top_container.setLayout(top_layout)

        root_layout.addWidget(top_container)
        root_layout.addWidget(self.bin_value_container, 0, Qt.AlignmentFlag.AlignRight)

        self.setLayout(root_layout)

    def handle_add_bin(self):
        result = self.range_input.get_bin_value()
        if result:
            self.bin_value_container.add_bin(result[0], result[1])
