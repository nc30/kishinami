from logging import getLogger
logger = getLogger(__name__)

from uuid import getnode
from kishinami import __version__
import subprocess
import socket

def getClientInfo():
    return {
        "kishinamiVersion": __version__,
        "macAddress": getMyMac(),
        "Host": getMyHost(),
        "Cpu": getCpuInfo()
    }

def getMyMac():
    node = getnode()
    return ':'.join([hex(node >> i & 0xff)[2:] for i in reversed(range(0, 48, 8))])

def getMyHost():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host = s.getsockname()[0]
        s.close()
    except OSError:
        host = 'unknown'
    return host

def getCpuInfo():
    return {
        "tempture": subprocess.check_output(['vcgencmd','measure_temp']).decode().strip().split("=")[1],
        "clock": subprocess.check_output(['vcgencmd','measure_clock arm']).decode().strip().split('=')[1],
        "voltage": subprocess.check_output(['vcgencmd', 'measure_volts']).decode().strip().split('=')[1],
        "arm_memoly_usage": subprocess.check_output(['vcgencmd', 'get_mem', 'arm']).decode().strip().split('=')[1],
        "gpu_memory_usage": subprocess.check_output(['vcgencmd', 'get_mem', 'gpu']).decode().strip().split('=')[1]
    }
