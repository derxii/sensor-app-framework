from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from PySide6.QtCore import QCoreApplication, Qt

import sys

from .widgets.MainWindow import MainWindow

def main():
    app = QApplication([])

    init_ui(app)
    w = MainWindow(960, 576, app.primaryScreen().availableGeometry().center())

    w.show()
    sys.exit(app.exec())

def init_ui(app: QApplication):
    font = QFont()
    font.setFamily("Times")
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

    app.setFont(font)

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app.setStyle("fusion")

    style_path = Path(__file__).parent.joinpath("style.qss")
    with open(style_path) as f:
        app.setStyleSheet(f.read())