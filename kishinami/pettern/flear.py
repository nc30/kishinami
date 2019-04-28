from logging import getLogger
logger = getLogger(__name__)

import colorsys
import math
from kishinami import WHITE, YELLOW, ORANGE, RED, BLUE


class Flear:
    def __init__(self, step=16, mask=4, low=0, limit=255):
        self.step = step
        self.limit = limit
        self.low = low
        self.power = self.low
        self.mask = mask

    def clock(self):
        self.power += self.step
        if self.low >= self.power or self.power >= self.limit:
            self.step = -self.step
        self.power = max(min(self.power, self.limit), self.low)
        return (
            self.power if self.mask & 4 else 0,
            self.power if self.mask & 2 else 0,
            self.power if self.mask & 1 else 0,
        )

    def reset(self):
        self.power = 0
        self.step = abs(self.step)

class Flear2(Flear):
    def __init__(self, start=0, color=ORANGE, speed=8):
        self.setColor(color)
        self.speed = speed
        self.power = start * 360

    def setColor(self, rgb):
        self.color = colorsys.rgb_to_hsv(*[c/255 for c in rgb])[:2]

    def clock(self):
        self.power += self.speed
        if self.power > 360:
            self.power = 0

        buf = 3

        m = math.cos(math.radians(self.power))
        s = abs(math.cos(math.radians(self.power * 4)) / 2)
        v = ((abs(m) + abs(s))) ** buf / (1.5 ** buf)
        return [int(c * 255) for c in colorsys.hsv_to_rgb(*self.color, v)]

    def reset(self):
        self.power = 0
