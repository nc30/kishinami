import logging
logger = logging.getLogger('kishinami')

from kishinami import WHITE
from .blink import Blink
from .flear import Flear, Flear2

class Null:
    def clock(self):
        return WHITE
