from logging import getLogger
logger = getLogger(__name__)

from kishinami import WHITE, YELLOW

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
