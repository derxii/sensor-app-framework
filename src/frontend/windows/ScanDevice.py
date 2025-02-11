from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QApplication
from PySide6.QtGui import Qt, QFont
from PySide6.QtCore import QTimer, QThread
from typing import Callable
import asyncio
import qasync


from frontend.config import (
    get_backend,
    handle_exception,
    is_debug,
)

from frontend.DebugData import get_debug_scan_devices
from frontend.thread.Worker import Worker
from frontend.widgets.Loader import Loader
from frontend.windows.Devices import Devices
from frontend.windows.ScrollableWindow import ScrollableWindow

def getScannedDevices(future):
        print(f"Result: {future.result()}")


class ScanDevice(ScrollableWindow):
    def __init__(self, switch_window: Callable[[QWidget], None]):
        super().__init__(switch_window)
        self.title = QLabel("Scanning for Bluetooth Devices")
        self.loader = Loader(256)
        self.description = QLabel("Please wait for up to 10 seconds...")
        self.init_ui()

        #self.thread = QThread()
        #asyncio.run(self.trigger_bluetooth_scan())
        
        task = asyncio.create_task(self.trigger_bluetooth_scan())
        #self.trigger_bluetooth_scan()
         
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_font = QFont()
        title_font.setPointSize(40)
        title_font.setWeight(QFont.Weight.DemiBold)
        self.title.setFont(title_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.loader.start_animation()
        layout.addWidget(self.loader)

        description_font = QFont()
        description_font.setPointSize(20)
        self.description.setFont(description_font)
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description)

        self.bind_scroll(layout)

    
    async def trigger_bluetooth_scan(self):
        '''if is_debug():
            QTimer.singleShot(0, lambda: self.on_scan_end([]))
        else:
            self.worker = Worker(
                self.thread,
                get_backend().scanForDevices,
                lambda e: handle_exception(e, None, True),
            )
            self.worker.cancel_thread_on_timeout(15)
            self.worker.func_done.connect(self.on_scan_end)
            self.thread.start()'''
        #loop = asyncio.new_event_loop()
        #app = QApplication.instance()
        #loop = qasync.QEventLoop(app)    
        #asyncio.set_event_loop(loop)
        #loop = asyncio.get_event_loop()
        #print(loop)


      
        #returnVal = await backend.scanForDevices() #loop.run_until_complete(backend.scanForDevices())
        #task = asyncio.create_task(get_backend().scanForDevices())
        backend = get_backend()
        try:
            returnVal = await backend.scanForDevices()
            self.on_scan_end(returnVal)
        except Exception as e:
            handle_exception(e, None, True),
       


    def on_scan_end(self, data: list[tuple[str, str, int]]):
        self.loader.stop_animation()
        if is_debug():
            data = get_debug_scan_devices()

        self.switch_window(
            Devices(self.switch_window, sorted(data, key=lambda d: (-d[2], d[0])))
        )
