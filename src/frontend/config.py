from pathlib import Path
from PySide6.QtWidgets import QStyleOption, QStyle, QWidget
from PySide6.QtGui import QPainter, QFontDatabase

resources_dir = Path(__file__).parent.parent.joinpath("resources")
default_width = 960
default_height = 576

def get_image_path(name: str):
    return str(resources_dir.joinpath(name))


def enable_custom_styling(widget: QWidget):
    opt = QStyleOption()
    opt.initFrom(widget) 
    painter = QPainter(widget)
    widget.style().drawPrimitive(QStyle.PE_Widget, opt, painter, widget)

def load_custom_font():
    font_path = str(resources_dir.joinpath("Roboto.ttf"))
    return QFontDatabase.addApplicationFont(font_path)