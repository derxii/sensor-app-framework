from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont

from frontend.config import enable_custom_styling


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frontend.widgets.DraggableResizable import DraggableResizable


class DraggableTopBar(QWidget):
    def __init__(self, parent: "DraggableResizable"):
        super().__init__()
        self.parent = parent

        self.drag_start_position = self.parent.pos()

        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.parent.destroy)

        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(15)
        self.close_button.setFixedSize(15, 15)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        button_font = QFont()
        button_font.setPointSizeF(10)
        button_font.setWeight(QFont.Weight.DemiBold)
        self.close_button.setFont(button_font)
        self.close_button.setObjectName("close-button")
        layout.addWidget(
            self.close_button,
            0,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
        )

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.drag_start_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.drag_start_position)
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.drag_start_position = event.globalPosition().toPoint()

    def paintEvent(self, _):
        enable_custom_styling(self)
