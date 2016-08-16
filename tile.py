from pygame import draw
from bullet import *

class Tile:
    def __init__(self, tile_name, color, size, hp=0, passable=True, light_source=False, tile_price=0):
        self.tile_name = tile_name
        self.hp = hp
        self.full_hp = hp
        self.color = color
        self.origc = color
        self.size = size
        self.passable = passable
        self.light_source = light_source
        self.emit_light = 0
        self.taking_dmg = False
        self.cooldown = 0
        self.tile_price = tile_price

    def update(self, dt):
        pass

    def add_light(self, amount):
        if self.emit_light <= 1:
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

    def attack(self, ox, oy, level, monsters, dt):
        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        if self.tile_name == 'Tower' and self.cooldown <= 0:
            for y in range(oy-4, oy+5):
                for x in range(ox-4, ox+5):
                    for m in monsters:
                        if m.x == x and m.y == y:
                            level.bullets.append(Bullet(m.x, m.y, ox, oy, 3, self.size))
                            self.cooldown = 4

    def take_dmg(self, amount):
        self.hp -= amount

        r = self.origc[0]
        g = self.origc[1]
        b = self.origc[2]

        r *= 1-amount/self.full_hp
        g *= 1-amount/self.full_hp
        b *= 1-amount/self.full_hp

        self.origc = (r , g, b)

    def draw(self, screen, x, y, xoff, yoff):
        draw.rect(screen, self.color, ((x+xoff)*self.size, (y+yoff)*self.size, self.size, self.size))
