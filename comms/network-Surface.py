import socket as s
import threading
import json
import time
from select import select

RUN = True
TIMEOUT = 1e-2
PORT = 12864


class diff_buffer:
    def __init__(self):
        self.buffer = []
        self.has_changed = False

    def add(self, to_add: str):
        if to_add not in self.buffer:
            self.has_changed = True
            self.buffer.append(to_add)
        else:
            self.has_changed = False

    def clear(self):
        self.buffer = []

    def as_string(self):
        string = json.dumps(self.buffer)
        self.has_changed = False
        return string


class endpoint:
    def __init__(self, base_port, addr="0.0.0.0", timeout=TIMEOUT):
        self.send_port = base_port
        self.recv_port = get_recv_port(base_port)
        self.addr = addr
        self.timeout = timeout


class lcl_endpoint(endpoint):
    def __init__(self, base_port, addr="0.0.0.0", timeout=TIMEOUT):
        super().__init__(base_port, addr, timeout)
        # socket creation
        self.send_socket, self.recv_socket = setup_sockets(base_port, addr)
        # thread spawning and release
        self.send_thread, self.recv_thread = setup_threads(
            self.send_socket, self.recv_socket
        )

    def poll_endpoint(self, other_endpoint):
        self.send_sock.send()

def get_recv_port(base_port):
    return base_port + 1


def thread_send_task(
        sock: s.socket, buffer: diff_buffer, timeout: float = TIMEOUT
        ):
    while RUN:
        rlist, wlist, xlist = select(
            [], [sock], [sock], timeout
        )
        if buffer.has_changed:
            for sock in wlist:
                sock.write(buffer.as_string())


def thread_recv_task(
        sock: s.socket, buffer: diff_buffer, timeout: float = TIMEOUT
        ):
    while RUN:
        rlist, wlist, xlist = select(
            [sock], [], [sock], timeout
        )
        for sock in rlist:
            addr, content = sock.read()
            buffer.add(content)


def _setup_socket(port, addr="0.0.0.0"):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM, s.IPPROTO_UDP)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, True)
    # sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEPORT, True)
    sock.setblocking(False)
    sock.bind((lcl_addr, portNo))
    return sock


def setup_sockets(base_port, addr="0.0.0.0"):
    send_sock = _setup_socket(base_port, addr)
    recv_sock = _setup_socket(get_recv_port(base_port), addr)
    return send_sock, recv_sock


def _setup_thread(direction, sock):
    dir_num = 0
    if direction == "send":
        thread_task = thread_send_task
    elif direction == "recv":
        dir_num += 1
        thread_task = thread_recv_task
    buffer = diff_buffer()
    kwargs = {
        "sock": sock,
        "buffer": buffer
    }
    thread = threading.Thread(target=thread_task, kwargs=kwargs)
    thread.start()


def setup_threads(send_sock, recv_sock):
    send_thread = _setup_thread("send", send_sock)
    recv_thread = _setup_thread("recv", recv_sock)
    return send_thread, recv_sock
