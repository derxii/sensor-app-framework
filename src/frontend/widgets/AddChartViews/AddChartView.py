from abc import abstractmethod
from PySide6.QtWidgets import QWidget, QSizePolicy, QLabel, QHBoxLayout, QLineEdit
from PySide6.QtGui import QFont, Qt


class AddChartView(QWidget):
    def create_text_input(self, label: str):
        font = self.get_form_font()

        label_widget = QLabel(f"{label}: ")
        label_widget.setFont(font)

        user_input = QLineEdit()
        user_input.setFont(font)

        container = self.set_left_right_aligned_widgets(label_widget, user_input, 1, 1)
        container.setFixedHeight(50)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return container, user_input

    @abstractmethod
    def on_submit_create(self) -> tuple[bool, int]:
        pass

    def get_form_font(self):
        font = QFont()
        font.setPointSizeF(16)
        return font

    def set_left_right_aligned_widgets(
        self,
        left_widget: QWidget,
        right_widget: QWidget,
        left_stretch: int = 1,
        right_stretch: int = 1,
    ):
        container = QWidget()

        layout = QHBoxLayout()

        layout.addWidget(
            left_widget,
            left_stretch,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
        )
        layout.addWidget(right_widget, right_stretch, Qt.AlignmentFlag.AlignTop)

        container.setLayout(layout)
        return container
