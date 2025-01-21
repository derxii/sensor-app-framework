from pathlib import Path
from PySide6.QtWidgets import QStyleOption, QStyle, QWidget
from PySide6.QtGui import QPainter, QFontDatabase
from PySide6.QtCore import QCoreApplication


from backend.Backend import Backend

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


def dynamically_repaint_widget(*widgets: QWidget):
    for widget in widgets:
        widget.style().polish(widget)
        widget.style().unpolish(widget)
        widget.update()


def load_custom_font():
    font_path = str(resources_dir.joinpath("Roboto.ttf"))
    return QFontDatabase.addApplicationFont(font_path)


def is_debug():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", "-d", action="store_true", help="Use mock data")

    args = parser.parse_args()
    return args.debug


def get_debug_scan_devices():
    data = [
        ("Arduino HC-06", "M9SK1K31-252D-43E3-A986-DCF3CB63D08", -50) for _ in range(33)
    ]
    data += [("long device name", "NDKA92N-24124-1241", 9)]
    return data


def set_backend():
    QCoreApplication.instance().setProperty("backend", Backend())


def get_backend() -> Backend:
    return QCoreApplication.instance().property("backend")
