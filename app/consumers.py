import asyncio
import threading
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from app.models import Program, ProgramAction
from subprocess import *
from hiverlab_py_simulator.settings import RUNNING_PROCESSES
from app.threads import *


class RunProgram(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.program = None
        self.out_stream = None
        self.in_stream = None
        self.err_stream = None
        self.process = None
        self.data_capture = DataCapture()
        self.error_capture = DataCapture()
        self.data_thread_controller = ThreadController()
        self.error_thread_controller = ThreadController()

    async def websocket_connect(self, event):
        await self.accept()
        self.program = await self.get_program()
        await self.send_data(ProgramAction(ProgramAction.ACTION_START, {}))
        if self.program.custom_args is not None and self.program.custom_args is not "":
            self.process = Popen(['python', self.program.file.path, self.program.custom_args], stdin=PIPE,
                                 stdout=PIPE, stderr=PIPE, bufsize=10)
        else:
            self.process = Popen(['python', self.program.file.path], stdin=PIPE,
                                 stdout=PIPE, stderr=PIPE, bufsize=10)
        self.out_stream = self.process.stdout
        self.in_stream = self.process.stdin
        self.err_stream = self.process.stderr
        threading.Thread(target=reader_capture,
                         args=(self.out_stream, self.process, self.data_capture, self.data_thread_controller,
                               self.send_data,)).start()
        threading.Thread(target=reader_capture,
                         args=(self.err_stream, self.process, self.error_capture,
                               self.error_thread_controller, self.send_data,)).start()
        threading.Thread(target=text_capture,
                         args=(self.data_capture, self.send_data, ProgramAction.ACTION_OUTPUT, self.process,
                               self.data_thread_controller,)).start()
        threading.Thread(target=text_capture,
                         args=(
                             self.error_capture, self.send_data, ProgramAction.ACTION_OUTPUT_ERROR,
                             self.process, self.error_thread_controller,)).start()

    async def websocket_receive(self, event):
        data = ProgramAction.received(obj=event['text'])
        if data.action == ProgramAction.ACTION_INPUT and self.process.poll() is None:
            self.in_stream.write(bytes(data.data, 'utf-8') + b'\n')
            self.in_stream.flush()

    async def websocket_disconnect(self, event):
        self.data_thread_controller.stop()
        self.error_thread_controller.stop()
        self.process.kill()

    @database_sync_to_async
    def get_program(self):
        return Program.objects.filter(pk=self.scope['url_route']['kwargs']['id'])[0]

    async def send_data(self, program_action):
        await self.send(
            {
                "type": "websocket.send",
                "text": program_action.send()
            }
        )
        await asyncio.sleep(0.0001)

    async def accept(self):
        await self.send({
            "type": "websocket.accept"
        })


class AlwaysRunProgram(AsyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.program = None
        self.out_stream = None
        self.in_stream = None
        self.err_stream = None
        self.process = None
        self.is_end = False
        self.data_capture = DataCapture()
        self.error_capture = DataCapture()
        self.data_thread_controller = ThreadController()
        self.error_thread_controller = ThreadController()

    async def websocket_connect(self, event):
        await self.accept()
        self.program = await self.get_program()
        await self.send_data(ProgramAction(ProgramAction.ACTION_PROCESS_RUNNING,
                                           RUNNING_PROCESSES.get(self.program.id, None) is not None))
        running_process = RUNNING_PROCESSES.get(self.program.id, None)
        if running_process is not None:
            self.process = running_process
            self.out_stream = self.process.stdout
            self.in_stream = self.process.stdin
            self.err_stream = self.process.stderr
            threading.Thread(target=reader_capture,
                             args=(self.out_stream, self.process, self.data_capture, self.data_thread_controller,
                                   self.send_data,)).start()
            threading.Thread(target=reader_capture,
                             args=(self.err_stream, self.process, self.error_capture,
                                   self.error_thread_controller, self.send_data,)).start()
            threading.Thread(target=text_capture,
                             args=(self.data_capture, self.send_data, ProgramAction.ACTION_OUTPUT, self.process,
                                   self.data_thread_controller,)).start()
            threading.Thread(target=text_capture,
                             args=(
                                 self.error_capture, self.send_data, ProgramAction.ACTION_OUTPUT_ERROR,
                                 self.process, self.error_thread_controller,)).start()
            await self.send_data(ProgramAction(ProgramAction.ACTION_START, ''))

    async def websocket_receive(self, event):
        data = ProgramAction.received(obj=event['text'])
        if data.action == ProgramAction.ACTION_START:
            running_process = RUNNING_PROCESSES.get(self.program.id, None)
            if running_process is not None:
                self.process = running_process
            else:
                if self.program.custom_args is not None and self.program.custom_args is not "":
                    self.process = Popen(['python', self.program.file.path, self.program.custom_args], stdin=PIPE,
                                         stdout=PIPE, stderr=PIPE, bufsize=10)
                else:
                    self.process = Popen(['python', self.program.file.path], stdin=PIPE,
                                         stdout=PIPE, stderr=PIPE, bufsize=10)
            self.out_stream = self.process.stdout
            self.in_stream = self.process.stdin
            self.err_stream = self.process.stderr
            threading.Thread(target=reader_capture,
                             args=(self.out_stream, self.process, self.data_capture, self.data_thread_controller,
                                   self.send_data,)).start()
            threading.Thread(target=reader_capture,
                             args=(self.err_stream, self.process, self.error_capture,
                                   self.error_thread_controller, self.send_data,)).start()
            threading.Thread(target=text_capture,
                             args=(self.data_capture, self.send_data, ProgramAction.ACTION_OUTPUT, self.process,
                                   self.data_thread_controller,)).start()
            threading.Thread(target=text_capture,
                             args=(
                                 self.error_capture, self.send_data, ProgramAction.ACTION_OUTPUT_ERROR,
                                 self.process, self.error_thread_controller,)).start()
            await self.send_data(ProgramAction(ProgramAction.ACTION_START, ''))
        else:
            if data.action == ProgramAction.ACTION_INPUT and self.process.poll() is None:
                self.in_stream.write(bytes(data.data, 'utf-8') + b'\n')
                self.in_stream.flush()
            if data.action == ProgramAction.ACTION_END:
                self.is_end = True
                self.process.kill()
                try:
                    RUNNING_PROCESSES[self.program.id] = None
                except:
                    pass

    async def websocket_disconnect(self, event):
        if not self.is_end:
            RUNNING_PROCESSES[self.program.id] = self.process
            self.data_thread_controller.stop()
            self.error_thread_controller.stop()

    @database_sync_to_async
    def get_program(self):
        return Program.objects.filter(pk=self.scope['url_route']['kwargs']['id'])[0]

    async def send_data(self, program_action):
        await self.send(
            {
                "type": "websocket.send",
                "text": program_action.send()
            }
        )
        await asyncio.sleep(0.0001)

    async def accept(self):
        await self.send({
            "type": "websocket.accept"
        })
