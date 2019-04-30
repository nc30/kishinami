from logging import getLogger
logger = getLogger(__name__)

from kishinami.pattern import Null, Flear
from kishinami import ORANGE, BLUE, YELLOW, RED, GREEN
from kishinami import NORMAL, WARNING, SIREN, PROGRESSING
from kishinami import action
from threading import Thread
import blinkt
import time

class Base(Thread):
    buf = 0
    leds = [None for i in range(blinkt.NUM_PIXELS)]
    currentColor = YELLOW

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)

        self.color = ORANGE
        self.loop = True
        self.normal = True
        self.clock = 0
        self.setState(PROGRESSING)

    def setState(self, state):
        if state == NORMAL:
            blinkt.set_brightness(0.1)
            for num in range(blinkt.NUM_PIXELS):
                self.leds[num] = Flear(start=num / blinkt.NUM_PIXELS, speed=8, lowest=0.2)
                self.color = self.currentColor
        elif state == SIREN:
            blinkt.set_brightness(0.3)
            for num in range(blinkt.NUM_PIXELS):
                self.leds[num] = Flear(start=num / blinkt.NUM_PIXELS, speed=60, buf=5, sub=0)
                self.color = RED
        elif state == PROGRESSING:
            blinkt.set_brightness(0.1)
            for num in range(blinkt.NUM_PIXELS):
                self.leds[num] = Flear(start=num / blinkt.NUM_PIXELS, speed=30, sub=3, buf=2)
                self.color = [20, 0, 85]
        else:
            blinkt.set_brightness(0.2)
            for num in range(blinkt.NUM_PIXELS):
                self.leds[num] = Flear(start=num / blinkt.NUM_PIXELS, speed=8)
                self.color = ORANGE

        self.setColor(self.color)

    def setColor(self, color, mask=255, blink=0):
        logger.debug('setcolor %s, %s', color, mask)
        for i in range(blinkt.NUM_PIXELS):
            if mask & 1 << i:
                self.leds[i].setColor(color)
                self.leds[i].blink = blink

    def run(self):
        while self.loop:
            if self.normal:
                self.write()
            time.sleep(0.01)

        time.sleep(0.02)
        blinkt.clear()
        time.sleep(0.02)
        blinkt.show()

    def write(self):
        self.clock += 1
        if self.clock > 360:
            self.clock = 0

        blinkt.clear()

        for num in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(num, *self.leds[num].clock(self.clock))
        blinkt.show()

    def shock(self, color):
        self.normal = False
        action.shock.run(color)
        self.normal = True

    def destroy(self):
        self.loop = False
        time.sleep(0.1)



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
