from logging import getLogger
logger = getLogger(__name__)

from uuid import getnode
from kishinami import __version__
import socket

def getClientInfo():
    return {
        "kishinamiVersion": __version__,
        "macAddress": getMyMac(),
        "Host": getMyHost()
    }

def getMyMac():
    node = getnode()
    return ':'.join([hex(node >> i & 0xff)[2:] for i in reversed(range(0, 48, 8))])

def getMyHost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host
