import colorsys

class Color(object):
    red = 0
    green = 0
    blue = 0

    def __init__(self, *args):
        try:
            if type(args[0]) == tuple or type(args[0]) == list:
                args = args[0][:3]
        except IndexError:
            raise TypeError()

        if len(args) <= 3:
            self.red = args[0]
            self.green = args[1] if len(args) >= 2 else 0
            self.blue = args[2] if len(args) >= 3 else 0


    def __getattr__(self, key):
        if key == 'rgb':
            return self.red, self.green, self.blue
        if key == 'hsv':
            return colorsys.rgb_to_hsv(self.red/255, self.green/255, self.blue/255)
        if key == 'list':
            return [self.red, self.green, self.blue]
        raise AttributeError

    def __str__(self):
        return "<RGB RED:"+str(self.red)+" GREEN:"+str(self.green)+" BLUE:"+str(self.blue)+">"
