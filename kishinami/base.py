from logging import getLogger
logger = getLogger(__name__)

import blinkt
from threading import Thread
import time
from .action import shock
from .pettern import Null, Flear, Flear2
from . import ORANGE

class Base(Thread):
    buf = 0
    leds = [None for i in range(blinkt.NUM_PIXELS)]
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.3)

        for num in range(blinkt.NUM_PIXELS):
            self.leds[num] = Flear2(start=num / blinkt.NUM_PIXELS)

        self.loop = True
        self.normal = True

    def setColor(self, color, mask=255):
        for i in range(blinkt.NUM_PIXELS):
            if mask & (i + 1):
                self.leds[i].setColor(color)

    def run(self):
        self.color = ORANGE
        while self.loop:
            if self.normal:
                self.write()
            time.sleep(0.01)

        time.sleep(0.02)
        blinkt.clear()
        time.sleep(0.02)
        blinkt.show()

    def write(self):
        blinkt.clear()

        for num in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(num, *self.leds[num].clock())
        blinkt.show()

    def shock(self, color):
        self.normal = False
        shock.run(color)
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

