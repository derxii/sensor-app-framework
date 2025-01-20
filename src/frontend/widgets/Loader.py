from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QMovie, Qt
from PySide6.QtCore import QSize

from frontend.config import get_image_path

class Loader(QWidget):

    def __init__(self, size: int):
        super().__init__()
        self.loading_animation = QLabel()
        self.movie = QMovie(get_image_path("spinner.gif"))
        self.init_ui(size)

    def init_ui(self, size: int):
        layout = QVBoxLayout()
        self.movie.setScaledSize(QSize(size, size))
        self.loading_animation.setMovie(self.movie)
        self.loading_animation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.loading_animation)
        self.setLayout(layout)

    def stop_animation(self):
        self.movie.stop()
        self.loading_animation.setHidden(True)

    def start_animation(self):
        self.movie.start()
        self.loading_animation.setHidden(False)