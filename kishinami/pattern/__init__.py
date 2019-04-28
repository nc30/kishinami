import logging
logger = logging.getLogger('kishinami')

from kishinami import WHITE
from .blink import Blink
from .flear import Flear

class Null:
    def clock(self):
        return WHITE
