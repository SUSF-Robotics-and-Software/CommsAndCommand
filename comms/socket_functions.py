import socket as s
from os import platform
from collections import namedtuple

address = namedtuple('connection_address', ['address', 'port'])


class sock_mode:
    def __init__(self, sock_type, protocol):
        self.sock_type = sock_type
        self.protocol = protocol


UDP = sock_mode(s.SOCK_DGRAM, s.IPPROTO_UDP)
TCP = sock_mode(s.SOCK_STREAM, s.IPPROTO_TCP)
PLATFORM = platform()
print(platform)


# dgram ======================================================================


def make_socket(addr: address, mode: _mode):
    sock = s.socket(s.AF_INET, mode.sock_type, mode.sock_type)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    if 'Linux' in platform:
        sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEPORT, 1)
