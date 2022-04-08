import time

import socketio
from locust import HttpUser, TaskSet, task, between, events


class SendMsg(TaskSet):
    wait_time = between(1, 2)

    def __init__(self, parent):
        super().__init__(parent)
        self.sio = socketio.Client()

    def on_start(self):
        self.sio.connect("http://127.0.0.1:8080/")

    def on_quit(self):
        self.sio.disconnect()

    @task(1)
    def send_message(self):
        start_at = time.time()
        body = "你好"
        self.sio.emit("chat-request", body)
        events.request_success.fire(
            request_type="WebSocket Sent",
            name="send 你好",
            response_time=int((time.time() - start_at)*1000000),
            response_length=len(body),
        )


class ManyUser(HttpUser):
    tasks = [SendMsg]
    min_wait = 0
    max_wait = 100
