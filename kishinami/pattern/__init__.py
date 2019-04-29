import logging
logger = logging.getLogger('kishinami')

from kishinami import WHITE
from .flear import Flear

class Null:
    def clock(self):
        return WHITE
