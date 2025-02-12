from PySide6.QtWidgets import QDockWidget, QWidget


class SquareDockWidget(QDockWidget):
    def resizeEvent(self, event):
        size = min(event.size().width(), event.size().height())
        self.resize(size, size)
        super().resizeEvent(event)

def on_change_level(is_floating: bool, contained_widget: QWidget):
    if is_floating:
        contained_widget.setObjectName("")
    else:
        contained_widget.setObjectName("dock-container")

    from frontend.config import dynamically_repaint_widget
    dynamically_repaint_widget(contained_widget)