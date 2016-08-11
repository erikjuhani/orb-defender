from pygame import draw

class Tile:
    def __init__(self, pos, tile_name, color, size, passable=True, light_source=False):
        self.x = pos[0]
        self.y = pos[1]
        self.tile_name = tile_name
        self.color = color
        self.origc = color
        self.size = size
        self.passable = passable
        self.light_source = light_source
        self.emit_light = 0

    def set_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def add_light(self, amount):
        if self.emit_light < 1:
            self.emit_light += amount

    def change_brightness(self, amount, tint=None):

        amount = amount + self.emit_light

        r = self.origc[0]
        g = self.origc[1]
        b = self.origc[2]

        max_r = r
        max_g = g
        max_b = b

        min_r = r * 0.01
        min_g = g * 0.01
        min_b = b * 0.01

        r *= amount
        g *= amount
        b *= amount

        if not tint == None:
            if 'r' in tint:
                r += r * amount
            if 'g' in tint:
                g += g * amount
            if 'b' in tint:
                b += b * amount

        if r < min_r:
            r = min_r
        if g < min_g:
            g = min_g
        if b < min_b:
            b = min_b

        if r > max_r:
            r = max_r
        if g > max_g:
            g = max_g
        if b > max_b:
            b = max_b

        self.color = (r, g, b)

    def draw(self, screen, xoff, yoff):
        draw.rect(screen, self.color, ((self.x+xoff)*self.size, (self.y+yoff)*self.size, self.size, self.size))
