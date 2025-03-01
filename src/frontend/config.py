import argparse
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
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()


def load_custom_font():
    font_path = str(resources_dir.joinpath("Roboto.ttf"))
    return QFontDatabase.addApplicationFont(font_path)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-virtual", "-v", type=str, help="Use virtual port at specified location"
    )
    return parser.parse_args()

def get_virtual_port():
    return parse_args().virtual


def set_backend():
    QCoreApplication.instance().setProperty("backend", Backend())


def get_backend() -> Backend:
    return QCoreApplication.instance().property("backend")


def set_switch_window(switch_window: Callable[[QWidget], None]):
    QCoreApplication.instance().setProperty("switch_window", switch_window)


def get_switch_window() -> Callable[[QWidget], None]:
    return QCoreApplication.instance().property("switch_window")


def handle_exception(
    e: Exception,
    message: Optional[str] = None,
    critical_error: Optional[bool] = False,
    description: str = None,
):
    print("ERROR: " + str(e))

    message_box = QMessageBox()
    message_box.setWindowTitle("Error")
    message_box.setText(
        f"{'Fatal ' if critical_error else ''}Error: {message if message else str(e)}"
    )
    message_box.setInformativeText(description if description else "Please try again.")
    message_box.setIconPixmap(QIcon(get_image_path("icon.svg")).pixmap(QSize(64, 64)))
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
    message_box.exec()

    if critical_error:
        from frontend.windows.Welcome import Welcome

        get_switch_window()(Welcome(get_switch_window()))
