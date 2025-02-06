from PySide6.QtWidgets import QDockWidget

class SquareDockWidget(QDockWidget):
    def resizeEvent(self, event):
        size = min(event.size().width(), event.size().height())
        self.resize(size, size)
        super().resizeEvent(event)