from PySide6.QtWidgets import QMainWindow, QWidget, QSystemTrayIcon
from PySide6.QtGui import QIcon
from PySide6.QtCore import QPoint


from frontend.helper import get_image_path
from frontend.widgets.Welcome import Welcome

class MainWindow(QMainWindow):
    def __init__(self, width: int, height: int, center: QPoint):
        super().__init__()
        self.init_ui(width, height, center)

        self.central_widget = Welcome(self.switch_central_widget)
        self.setCentralWidget(self.central_widget)

        self.tray_icon.activated.connect(self.raise_)


    def init_ui(self, width: int, height: int, center: QPoint):
        self.resize(width, height)
        self.setMinimumSize(width // 2, height // 2)
        self.move(center.x() - width // 2, center.y() - height // 2)

        self.setWindowIcon(QIcon(get_image_path("icon.svg")))
        self.setWindowTitle("Sensor Data Visualiser")
        
        self.tray_icon = QSystemTrayIcon(QIcon(get_image_path("icon.svg")))
        self.tray_icon.show()


    def switch_central_widget(self, widget: QWidget):
        self.central_widget = widget
        self.setCentralWidget(self.central_widget)


    def show_notification(self):
        self.tray_icon.showMessage("title", "message", QIcon(get_image_path("icon.svg")), 3000)