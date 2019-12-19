import socket as s
import threading
import json
import time
from select import select
from .buffers import diff_buffer

RUN = True
TIMEOUT = 1e-2
PORT = 12864


class endpoint:
    def __init__(self, base_port, addr, timeout=TIMEOUT):
        self.send_port = base_port
        self.recv_port = get_recv_port(base_port)
        self.addr = addr
        self.timeout = timeout


class lcl_endpoint(endpoint):
    def __init__(
            self, base_port, addr="0.0.0.0", timeout=TIMEOUT,
            buffer_type=diff_buffer
            ):
        super().__init__(base_port, addr, timeout)
        # buffer creation
        self.send_buffer = buffer_type()
        self.recv_buffer = buffer_type()
        # socket creation
        self.send_socket = setup_socket(base_port)
        self.recv_socket = setup_socket(get_recv_port(base_port), addr)

        self.toaddr = None
        self.send_thread = None
        self.recv_thread = None

    def start_service(self, toaddr):
        self.send_thread, self.recv_thread = setup_threads(
            self.send_socket, self.recv_socket,
            self.send_buffer, self.recv_buffer
        )

    def poll_address(self, port, addr):
        if remote_socket is None and remote is None:
            raise ValueError("Must pass a remote to poll, either:\ntuple(addr, port)\nendpoint object")
        self.send_buffer

    def get_send_args(self):
        self.send_socket, self.send_buffer, self.toaddr


def get_recv_port(base_port):
    return base_port + 1


def thread_send_task(
        service_ep: lcl_endpoint
        ):
    while RUN:
        rlist, wlist, xlist = select(
            [], [sock], [sock], timeout
        )
        if buffer.has_changed:
            for sock in wlist:
                sock.send(buffer.as_string())


def thread_recv_task(
        service_ep: lcl_endpoint
        ):
    while RUN:
        rlist, wlist, xlist = select(
            [sock], [], [sock], timeout
        )
        for sock in rlist:
            addr, content = sock.read()
            buffer.add(content)


def setup_socket(port, addr="0.0.0.0"):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM, s.IPPROTO_UDP)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, True)
    # sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEPORT, True)
    sock.setblocking(False)
    sock.bind((lcl_addr, portNo))
    return sock


def _setup_thread(direction, sock, buffer):
    if direction == "send":
        thread_task = thread_send_task
    elif direction == "recv":
        thread_task = thread_recv_task
    kwargs = {
        "sock": sock,
        "buffer": buffer
    }
    thread = threading.Thread(target=thread_task, kwargs=kwargs)
    thread.start()


def setup_threads(send_sock, recv_sock, send_buffer, recv_buffer):
    send_thread = _setup_thread("send", send_sock, send_buffer)
    recv_thread = _setup_thread("recv", recv_sock, recv_buffer)
    return send_thread, recv_thread
