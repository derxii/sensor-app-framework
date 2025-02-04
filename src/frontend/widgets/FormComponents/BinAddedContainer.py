from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QFrame
from PySide6.QtGui import Qt


from frontend.config import get_image_path
from frontend.widgets.Button import Button
from frontend.windows.ScrollableWindow import ScrollableWindow


class BinAddedContainer(ScrollableWindow):
    def __init__(self):
        super().__init__(None)
        self.bins: list[tuple[float, float]] = []

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(200, 250)
        self.scroll_area.setObjectName("bordered")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.bind_scroll(self.layout)

    def add_bin(self, lower_value: float, upper_value: float):
        self.bins.append((lower_value, upper_value))
        self.bins.sort(key=lambda range: range[0])
        self.refresh_bin_ui()

    def refresh_bin_ui(self):
        for _ in range(self.layout.count()):
            widget = self.layout.itemAt(0).widget()
            widget.setParent(None)
            widget.deleteLater()

        for i, (lower_value, upper_value) in enumerate(self.bins):
            widget = self.create_bin_created_widget(lower_value, upper_value, i)
            self.layout.addWidget(widget)

            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.HLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            self.layout.addWidget(separator)

        self.layout.addWidget(QWidget(), 1000)

    def create_bin_created_widget(
        self, lower_value: float, upper_value: float, index: int
    ):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        label = QLabel(f"{lower_value} - {upper_value} ")
        layout.addWidget(label)

        delete_button = Button("", get_image_path("bin.svg"), "bin")
        delete_button.clicked.connect(lambda: self.delete_bin(index))
        layout.addWidget(delete_button, 0, Qt.AlignmentFlag.AlignRight)

        widget.setLayout(layout)

        return widget

    def delete_bin(self, index: int):
        self.bins.pop(index)
        self.refresh_bin_ui()

    def get_bins(self):
        return self.bins
