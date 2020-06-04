import socket as s
import threading
import json
import time
from collections import namedtuple
from select import select

connection_address = namedtuple('connection_address', ['address', 'port'])


class endpoint:
    """
        base clases for endpoints on the network

        do not use directly, create a subclass. You'll need to implement
        a get_connection function, which returns true if there is a
        connection and false if there is not. You will also need to create
        a thread_task function, which defines the continuous process of the
        thread.
    """
    def __init__(self, local_address):
        # things come *in* to the in box from the network
        self.in_box = []
        # things go *out* of the out box to the network
        self.out_box = []
        # holds the connection object to be read/written
        self.connection = None
        # whether or not a connection has been established.
        self.connected = False
        # inter-thread signal to tell client when to send
        self.out_box_populated = threading.Event()
        # the address of this machine in the form of the
        # named tuple "connection_address"
        self.local_address = local_address
        # the socket object
        self.sock = s.socket(s.AF_INET, s.SOCK_STREAM, s.IPPROTO_TCP)
        # if the socket doesn't get closed due to an error, this allows
        # for re-use. This is a bad way of handling it, but quick and
        # easy for testing. If the address is in use, we want a new port.
        self.sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        # self.sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEPORT, 1)
        # bind the socket to the local address
        self.sock.bind(local_address)
        # internal flag for the while loop, can be externally set; you
        # should use endpoint.stop() however
        self._stop = False
        # might want a send thread and a recieve thread, given they don't
        # really interact, and doing both at the same time requires order.
        self._thread = threading.Thread(target=self.thread_task)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop = True
        # print("network: closing connections with force")
        # if self.connection is not None:
        #     self.connection.close()
        # self.sock.close()

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
            # print(self.in_box)

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
        self._thread.name = "client"
        self.connection_target = connection_target

    def get_connection(self):
        if not self.connected:
            self.sock.connect(self.connection_target)
            self.connection = self.sock
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
        self._thread.name = "server"
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

    def recv_all(self):
        out = self.in_box
        self.in_box = []
        return out

    def recv(self):
        return self.in_box.pop(0)
