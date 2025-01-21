from pathlib import Path
from typing import Callable, Optional
from PySide6.QtWidgets import QStyleOption, QStyle, QWidget, QMessageBox
from PySide6.QtGui import QPainter, QFontDatabase, QIcon
from PySide6.QtCore import QCoreApplication, QSize


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


def set_switch_window(switch_window: Callable[[QWidget], None]):
    QCoreApplication.instance().setProperty("switch_window", switch_window)


def get_switch_window() -> Callable[[QWidget], None]:
    return QCoreApplication.instance().property("switch_window")


def handle_exception(e: Exception, message: Optional[str] = None):
    print(e)

    message_box = QMessageBox()
    message_box.setWindowTitle("Error")
    message_box.setText("Something went wrong!")
    message_box.setInformativeText(message if message else str(e))
    message_box.setIconPixmap(QIcon(get_image_path("icon.svg")).pixmap(QSize(64, 64)))
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
    message_box.exec()

    from frontend.windows.Welcome import Welcome

    get_switch_window()(Welcome(get_switch_window()))
