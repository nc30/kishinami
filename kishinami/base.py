from logging import getLogger
logger = getLogger(__name__)

import blinkt
from threading import Thread
import time

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (128, 128, 0)
WHITE = (0, 0, 0)
ORANGE = (255, 40, 0)

class Base(Thread):
    buf = 0
    leds = [None for i in range(blinkt.NUM_PIXELS)]
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.05)

        for num in range(blinkt.NUM_PIXELS):
            self.leds[num] = Flear2(start=num / blinkt.NUM_PIXELS)

        self.loop = True
        self.normal = True

    def setColor(self, color):
        for i in range(blinkt.NUM_PIXELS):
            self.leds[i].setColor(color)

    def run(self):
        self.color = ORANGE
        while self.loop:
            if self.normal:
                self.write()
                time.sleep(0.01)

        time.sleep(0.1)
        blinkt.clear()
        time.sleep(0.1)
        blinkt.show()

    def write(self):
        blinkt.clear()

        for num in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(num, *self.leds[num].clock())
        blinkt.show()

    def destroy(self):
        self.loop = False
        time.sleep(0.1)


class Blink:
    def __init__(self, colors=[WHITE, YELLOW], step=20):
        self.step = step
        self.colors = colors
        self.max = len(self.colors)
        self.state = self.max - 1
        self.buf = 0

    def clock(self):
        self.buf += 1
        if self.buf > self.step:
            self.buf = 0
            self.state += 1
            if self.state >= self.max:
                self.state = 0
        return self.colors[self.state]

    def reset(self):
        self.power = 0
        self.step = abs(self.step)


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

import colorsys
import math
class Flear2(Flear):
    def __init__(self, start=0, color=ORANGE, speed=8):
        self.setColor(color)
        self.speed = speed
        self.power = start * 360

    def setColor(self, rgb):
        print(rgb)
        self.color = colorsys.rgb_to_hsv(*[c/255 for c in rgb])[:2]

    def clock(self):
        self.power += self.speed
        if self.power > 360:
            self.power = 0

        m = math.cos(math.radians(self.power))
        s = abs(math.cos(math.radians(self.power * 2)) / 2)
        v = (abs(m) + abs(s)) / 2
        return [int(c * 255) for c in colorsys.hsv_to_rgb(*self.color, v)]

    def reset(self):
        self.power = 0

class Null:
    def clock(self):
        return WHITE


if __name__ == '__main__':
    import signal
    def handler(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, handler)

    import requests
    try:
        d = Base(daemon=True)
        d.start()

        before = 0
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        pass

    finally:
        print('bye')
        d.destroy()

