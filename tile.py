from pygame import *
from bullet import *

import math

class Tile:
    def __init__(self, x, y, tile_name, color, size, sprite=None, hp=0, passable=True, light_source=False, tile_price=0):
        self.tile_name = tile_name
        self.x = x
        self.y = y
        self.hp = hp
        self.full_hp = hp
        self.color = color
        self.origc = color
        self.size = size
        self.passable = passable
        self.light_source = light_source
        self.emit_light = 0
        self.cooldown = 0
        self.sprite = sprite
        if self.sprite != None:
            self.draw_sprite = transform.scale(self.sprite.img, (self.size, self.size))
        self.tile_price = tile_price
        self.surface = Surface((size, size))

    def update(self, dt):
        self.surface.fill(self.color)

    def return_rect(self):
        return Rect(0, 0, self.size, self.size)

    def add_light(self, amount):
        if self.emit_light <= 1:
            self.emit_light += amount

    def change_brightness(self, amount, pixel=None, tint=None):

        amount = amount + self.emit_light

        if pixel == None:
            r = self.origc[0]
            g = self.origc[1]
            b = self.origc[2]
        else:
            r, g, b, a = pixel

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

        if pixel == None:
            self.color = int(r), int(g), int(b)
        else:
            return int(r), int(g), int(b), a

    def change_img_brightness(self, amount, tint=None):

        pixel_array = PixelArray(self.sprite.img)
        size = len(pixel_array)

        for y in range(size):
            for x in range(size):
                pixel_array[x, y] = self.change_brightness(amount, self.sprite.unmapped_rgb[x + y * size], tint)

        del pixel_array

        self.draw_sprite = transform.scale(self.sprite.img, (self.size, self.size))

    def attack(self, ox, oy, level, monsters, dt):
        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        if self.tile_name == 'Tower' and self.cooldown <= 0:
            for m in monsters:
                xv = m.x - ox
                yv = m.y - oy
                distance = math.sqrt(xv*xv + yv*yv)

                if distance <= 5.1 and not m.flyer:
                    level.bullets.append(Bullet(m.x, m.y, ox, oy, 3, 10, (0, 0, 255), True, self.size))
                    self.cooldown = 6
                    break

        if self.tile_name == 'Air tower' and self.cooldown <= 0:
            for m in monsters:
                xv = m.x - ox
                yv = m.y - oy
                distance = math.sqrt(xv*xv + yv*yv)

                if distance <= 3.1:
                    level.bullets.append(Bullet(m.x, m.y, ox, oy, 4, 0.4, (0, 255, 0), True, self.size))
                    self.cooldown = 0.4
                    break

    def take_dmg(self, amount):
        self.hp -= amount

        self.change_img_brightness(self.hp/self.full_hp)

    def draw(self, screen, x, y, xoff, yoff):
        #draw.rect(screen, self.color, ((x+xoff)*self.size, (y+yoff)*self.size, self.size, self.size))
        if self.sprite != None:
            #sprite = transform.scale(self.sprite.img, (self.size, self.size))
            screen.blit(self.surface, ((x+xoff)*self.size, (y+yoff)*self.size))
            screen.blit(self.draw_sprite, ((x+xoff)*self.size, (y+yoff)*self.size), self.surface.get_rect())
        else:
            screen.blit(self.surface, ((x+xoff)*self.size, (y+yoff)*self.size))
