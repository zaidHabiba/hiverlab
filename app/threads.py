import time
import asyncio

from app.models import ProgramAction


class ThreadController:

    def __init__(self):
        self._stop = False

    def is_stop(self):
        return self._stop

    def stop(self):
        self._stop = True


class DataCapture:
    def __init__(self):
        self.data = []

    def add_data(self, d):
        self.data.append(d)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = [d for d in data]

    def clear(self):
        self.data = []


def text_capture(capture, send_data, action, process, thread_controller):
    local_capture = DataCapture()
    same_counter = 0
    while True:
        time.sleep(0.02)
        same_counter += 1 if capture.get_data() == local_capture.get_data() else 0
        local_capture.set_data(capture.get_data())
        if capture.get_data() == local_capture.get_data() and same_counter > 5 and local_capture.get_data() != []:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_data(
                ProgramAction(action, "".join([str(e, 'utf-8') for e in capture.get_data()]))))
            local_capture.clear()
            capture.clear()
            same_counter = 0
        if process.poll() is not None or thread_controller.is_stop():
            if local_capture.get_data():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(send_data(
                    ProgramAction(action, "".join([str(e, 'utf-8') for e in capture.get_data()]))))
            time.sleep(1)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_data(
                ProgramAction(ProgramAction.ACTION_END, '')))
            break


def reader_capture(stream, process, capture, thread_controller, send_data):
    while True:
        if stream is not None:
            stream.flush()
            value = stream.read(1)
            if value != b'':
                capture.add_data(value)
        if process.poll() is not None or thread_controller.is_stop():
            break
