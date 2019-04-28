import blinkt
import math
import colorsys
import time

def run(color=[255, 40, 0]):
    blinkt.clear()
    time.sleep(0.1)
    colors = colorsys.rgb_to_hsv(*[c/255 for c in color])[:2]

    for i in range(0, 720, 90):
        blinkt.clear()
        v = (math.cos(math.radians(i)))
        d = (blinkt.NUM_PIXELS / 2) + (v * blinkt.NUM_PIXELS / 2)

        for num in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(num, *[int(c * 255) for c in colorsys.hsv_to_rgb(*colors, min(1, max(d-num, 0)))] )

        blinkt.show()
        time.sleep(0.00001)

if __name__ == '__main__':
    run()
