import asyncio
from typing import Any, Coroutine
from PySide6.QtCore import QObject, Signal, QTimer, QThread


class Worker(QObject):
    func_done = Signal(object)
    exception = Signal(Exception)

    def __init__(
        self,
        thread: QThread,
        func: Coroutine[Any, Any, Any],
        exception_handlder,
        *args: any,
        **kwargs: any,
    ):
        super().__init__()
        self.thread = thread
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.sent_payload = False

        self.moveToThread(self.thread)
        self.exception.connect(exception_handlder)
        self.thread.started.connect(self.run)

    def run(self):
        try:
            asyncio.run(self.call_func_async())
        except Exception as e:
            print("Exception in backend: " + str(e))
            self.emit_error(e)

    def emit_error(self, e: Exception):
        if self.sent_payload:
            return
        self.sent_payload = True
        self.exception.emit(e)
        self.thread.quit()

    async def call_func_async(self):
        result = await self.func(*self.args, **self.kwargs)
        if self.sent_payload:
            return
        self.sent_payload = True
        self.func_done.emit(result)
        self.thread.quit()

    def cancel_thread_on_timeout(self, time_s: int):
        def cancel_ongoing_threads():
            self.emit_error(Exception("Timed Out"))

        QTimer.singleShot(time_s * 1000, cancel_ongoing_threads)
