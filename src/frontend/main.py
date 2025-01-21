from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import QCoreApplication, Qt
import PySide6.QtAsyncio as QtAsyncio

import sys

from .windows.MainWindow import MainWindow
from frontend.config import default_width, default_height, load_custom_font

def main():
    app = QApplication([])

    init_ui(app)
    w = MainWindow(default_width, default_height, app.primaryScreen().availableGeometry().center())

    w.show()
    sys.exit(QtAsyncio.run(handle_sigint = True))

def init_ui(app: QApplication):
    font_id = load_custom_font()

    custom_font = QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
    custom_font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
    custom_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

    app.setFont(custom_font)

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app.setStyle("fusion")

    style_path = Path(__file__).parent.joinpath("style.qss")
    with open(style_path) as f:
        app.setStyleSheet(f.read())