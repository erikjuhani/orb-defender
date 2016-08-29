from pygame import *
from sprite import *

import random

class Entity:
    def __init__(self, x, y, hp, size, color, sprite):
        self.x = int(x)
        self.y = int(y)
        self.hp = hp
        self.full_hp = hp
        self.size = size
        self.color = color
        self.origc = color
        self.remove = False
        self.sprite = sprite
        if self.sprite != None:
            self.draw_sprite = transform.scale(self.sprite.img, (self.size, self.size))
        self.surface = Surface((size, size))
        self.emit_light = 0

    def add_light(self, amount):
        if self.emit_light < 1:
            self.emit_light += amount

    def return_rect(self):
        return Rect(self.x, self.y, self.size, self.size)

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
                pixel_array[x, y] = self.change_brightness(amount, self.sprite.img.unmap_rgb(self.sprite.static_array[x, y]), tint)

        del pixel_array

        self.draw_sprite = transform.scale(self.sprite.img, (self.size, self.size))

    def update(self, dt):
        pass

    def draw(self, screen, xoff, yoff):
        #draw.rect(screen, self.color, ((self.x + xoff) * self.size, (self.y + yoff) * self.size, self.size, self.size))
        #sprite = transform.scale(self.sprite.img, (self.size, self.size))
        screen.blit(self.draw_sprite, ((self.x+xoff)*self.size, (self.y+yoff)*self.size), self.surface.get_rect())

class Monster(Entity):
    def __init__(self, x, y, speed, hp, size, color, dmg, flyer, spawner, sprite):
        super(self.__class__, self).__init__(x, y, hp, size, color, sprite)
        self.speed = speed
        self.cooldown = 0
        self.dmg = dmg
        self.flyer = flyer
        self.spawner = spawner
        if self.spawner:
            self.spawn_cooldown = 4

    def check_wall(self, level, locx, locy):
        if locx >= 0 and locx < level.map_size and locy >= 0 and locy < level.map_size:
            if level.terrain_map[locx + locy * level.map_size].tile_name == 'Heart':
                return False
            elif not level.terrain_map[locx + locy * level.map_size].passable and not self.flyer:
                return False
        return True

    def do_attack(self, level, locx, locy, dt):
        if self.flyer and level.terrain_map[locx + locy * level.map_size].tile_name == 'Heart':
            level.terrain_map[locx + locy * level.map_size].take_dmg(self.dmg)
        else:
            level.terrain_map[locx + locy * level.map_size].take_dmg(self.dmg)

    def take_dmg(self, dmg):

        if dmg > 0:
            self.hp -= dmg

    def update(self, dt):
        pass

    def spawn_child(self, level):
        x = random.randint(self.x-1, self.x+1)
        y = random.randint(self.y-1, self.y+1)
        level.monsters.append(Monster(x, y, random.randint(5, 7), 10, self.size, (114, 127, 79), 2, False, False, Sprite(textures['monster1'])))

    def simple_move(self, level, targetx, targety, dt):
        self.cooldown -= 1 * (self.speed/10) * dt

        if self.spawner:
            self.spawn_cooldown -= 1 * (self.speed/10) * dt

            if self.spawn_cooldown < 0:
                self.spawn_cooldown = 0

            if self.spawn_cooldown == 0:
                self.spawn_child(level)
                self.spawn_cooldown = 5

        if self.cooldown < 0:
            self.cooldown = 0

        if self.cooldown == 0:
            if targetx > self.x:
                if self.check_wall(level, self.x+1, self.y):
                    self.x += 1
                else:
                    self.do_attack(level, self.x+1, self.y, dt)
                self.cooldown = 1
            elif targetx < self.x:
                if self.check_wall(level, self.x-1, self.y):
                    self.x -= 1
                else:
                    self.do_attack(level, self.x-1, self.y, dt)
                self.cooldown = 1
            if targety > self.y:
                if self.check_wall(level, self.x, self.y+1):
                    self.y += 1
                else:
                    self.do_attack(level, self.x, self.y+1, dt)
                self.cooldown = 1
            elif targety < self.y:
                if self.check_wall(level, self.x, self.y-1):
                    self.y -= 1
                else:
                    self.do_attack(level, self.x, self.y-1, dt)
                self.cooldown = 1
