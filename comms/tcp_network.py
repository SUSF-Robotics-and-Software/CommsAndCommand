import socket as s
import threading
import json
import time
from collections import namedtuple
from select import select

connection_address = namedtuple('connection_address', ['address', 'port'])
THREAD_LIST = []


class endpoint:
    def __init__(self, local_address):
        # things come *in* to the in box
        self.in_box = []
        # things go *out* of the out box
        self.connection = None
        self.connected = False
        self.out_box = []
        self.out_box_populated = threading.Event()
        self.local_address = local_address
        self.sock = s.socket(s.AF_INET, s.SOCK_STREAM, s.IPPROTO_TCP)
        self.sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.sock.bind(local_address)

        self._stop = False
        # might want a send thread and a recieve thread, given they don't
        # really interact
        self._thread = threading.Thread(target=self.thread_task)
        THREAD_LIST.append(self._thread)

    def start(self):
        self._thread.start()

    def stop(self):
        self.sock.close()

    def get_connection(self):
        raise NotImplementedError("Implement a get_connection\
             method for the class to use")

    def thread_task(self):
        raise NotImplementedError("Implement a get_connection\
             method for the class to use")

    def _update_out_box(self, msg):
        self.out_box.append(msg)
        self.out_box_populated.set()

    def _process_buffers(self):
        readables, writables, errors = select(
            [self.connection], [self.connection], [self.connection]
        )
        for readable in readables:
            # recv might return an address too, check this...
            self.in_box.append(readable.recv(2048))
            print(self.in_box)

        did_send = False
        for writable in writables:
            while len(self.out_box) > 0:
                did_send = True
                msg = self.out_box.pop(0)
                if len(msg) > 0:
                    # print(f"sending: {msg}")
                    writable.send(bytes(msg, 'UTF-8'))
            if did_send:
                self.out_box_populated.clear()


class client(endpoint):
    def __init__(self, local_address, connection_target):
        super().__init__(local_address)
        self.connection_target = connection_target

    def get_connection(self):
        if not self.connected:
            self.sock.connect(self.connection_target)
            self.connection = self.sock
            # print("client: connected")
            self.connected = True
        return self.connected

    def send(self, msg):
        if msg not in self.out_box:
            self._update_out_box(msg)

    def thread_task(self):
        # print("client: started")
        while not self._stop:
            if self.get_connection():
                # print("client: waiting for outbox population")
                self.out_box_populated.wait()
                # print("client: outbox populated, sending")
                self._process_buffers()
        # print("client: stopped")


class server(endpoint):
    def __init__(self, local_address):
        super().__init__(local_address)
        self.sock.listen()

    def thread_task(self):
        # print("server: started")
        while not self._stop:
            if self.get_connection():
                self._process_buffers()
        # print("server: stopped")

    def get_connection(self):
        if not self.connected:
            self.connection, addr = self.sock.accept()
            # print(f"server: got a connection: {addr}")
            self.connected = True
        return self.connected

    def recv(self):
        return self.in_box
