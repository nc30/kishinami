from logging import getLogger
logger = getLogger(__name__)

import colorsys
import math
from kishinami import WHITE, YELLOW, ORANGE, RED, BLUE

class Flear:
    def __init__(self, start=0, color=ORANGE, speed=8, buf=1, sub=0, lowest=0, blink=0, low_light=False):
        self.setColor(color)
        self.speed = speed
        self.start = start * 360
        self.buf = buf
        self.sub = sub
        self.lowest = lowest
        self.blink = blink
        self.low_light = low_light

    def setColor(self, rgb):
        self.color = colorsys.rgb_to_hsv(*[c/255 for c in rgb])[:2]

    def clock(self, clock):
        if self.blink and clock % (360 / self.blink) > 360 / (self.blink * 2):
            return [int(c * 255) for c in colorsys.hsv_to_rgb(*self.color, 0.05)]

        clock = clock * self.speed + self.start

        m = abs(math.cos(math.radians(clock)))
        l = 1
        s = 0
        if self.sub:
            s = abs(math.cos(math.radians(clock * self.sub) / 2))
            l = 1.5
        if self.low_light:
            l += 2

        v = (self.lowest + m + s) ** self.buf / (self.lowest + l) ** self.buf
        return [int(c * 255) for c in colorsys.hsv_to_rgb(*self.color, v)]
