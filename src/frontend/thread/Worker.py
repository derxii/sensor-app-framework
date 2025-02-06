import asyncio
from typing import Any, Callable, Coroutine
from PySide6.QtCore import QObject, Signal, QTimer, QThread


class Worker(QObject):
    func_done = Signal(object)
    exception = Signal(Exception)

    def __init__(
        self,
        thread: QThread,
        func: Coroutine[Any, Any, Any],
        exception_handlder: Callable[[Exception], any],
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
            asyncio.run(self.main())
        except Exception as e:
            print("Exception in backend: " + str(e))
            self.emit_error(e)

    async def main(self):
        self.task = asyncio.create_task(self.call_func_async())
        try:
            await self.task
            self.stop()
        except asyncio.exceptions.CancelledError:
            print("Task Cancelled")

    def emit_error(self, e: Exception):
        if self.sent_payload:
            return
        self.sent_payload = True
        self.exception.emit(e)
        self.stop()

    async def call_func_async(self):
        result = await self.func(*self.args, **self.kwargs)
        if self.sent_payload:
            return
        self.sent_payload = True
        self.func_done.emit(result)
        self.stop()

    def cancel_thread_on_timeout(self, time_s: int):
        def cancel_ongoing_threads():
            self.emit_error(Exception("Timed Out"))

        QTimer.singleShot(time_s * 1000, cancel_ongoing_threads)

    def stop(self):
        self.task.cancel()
        self.thread.quit()
