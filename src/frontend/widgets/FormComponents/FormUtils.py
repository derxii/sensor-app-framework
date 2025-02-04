from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSizePolicy
from PySide6.QtGui import QFont, Qt


def create_text_input(label: str):
    font = get_form_font()

    label_widget = QLabel(f"{label}: ")
    label_widget.setFont(font)

    user_input = QLineEdit()
    user_input.setFont(font)

    container = set_left_right_aligned_widgets(label_widget, user_input, 1, 1)
    container.setFixedHeight(50)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return container, user_input


def get_form_font():
    font = QFont()
    font.setPointSizeF(16)
    return font


def set_left_right_aligned_widgets(
    left_widget: QWidget,
    right_widget: QWidget,
    left_stretch: int = 1,
    right_stretch: int = 1,
    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignVCenter,
):
    container = QWidget()

    layout = QHBoxLayout()

    layout.addWidget(
        left_widget,
        left_stretch,
        Qt.AlignmentFlag.AlignLeft | alignment,
    )
    layout.addWidget(right_widget, right_stretch, alignment)

    container.setLayout(layout)
    return container
