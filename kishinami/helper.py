from logging import getLogger
logger = getLogger(__name__)

import socket
import kishinami

def getClientInfo():
    return {
        "kishinamiVersion": kishinami.__version__,
        "macAddress": getMyMac(),
        "Host": getMyHost()
    }

def getMyMac():
    from uuid import getnode
    node = getnode()
    return ':'.join([hex(node >> i & 0xff)[2:] for i in reversed(range(0, 48, 8))])

def getMyHost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host
