from pygame import *
from key_dict import *

class Cursor:
    def __init__(self, x, y, size):
        self.x = int(x)
        self.y = int(y)
        self.size = size
        self.speed = 1
        self.cooldown = 0
        self.block = 0
        self.menu_switch = {'Build' : True}
        self.menu_block = {0 : 'Wall',
                 1 : 'Tower',
                 2 : 'Torch'}

    def check_border(self, level, location):
        if location < 0 or location >= level.map_size:
            return False
        return True

    def update(self, keys, level, dt):
        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        tile = level.terrain_map[self.x + self.y * level.map_size]

        for key in KEY_DICT:
            if keys[key] and self.cooldown == 0:
                if KEY_DICT[key] == 'left' and self.check_border(level, self.x - self.speed):
                        self.x -= self.speed
                if KEY_DICT[key] == 'right' and self.check_border(level, self.x + self.speed):
                        self.x += self.speed
                if KEY_DICT[key] == 'up' and self.check_border(level, self.y - self.speed):
                        self.y -= self.speed
                if KEY_DICT[key] == 'down' and self.check_border(level, self.y + self.speed):
                        self.y += self.speed
                if KEY_DICT[key] == 'switch':
                    self.menu_switch['Build'] = not self.menu_switch['Build']

                if KEY_DICT[key] == 'block':
                    self.block += 1
                    if self.block > 2:
                        self.block = 0

                if KEY_DICT[key] == 'action':
                    if self.menu_switch['Build'] and level.gold > 0:
                        if tile.passable:
                            level.create_tile(self.x, self.y, self.menu_block[self.block])
                    elif not self.menu_switch['Build']:
                        if not tile.passable:
                            level.break_tile(self.x, self.y)
                            level.gold += tile.tile_price
                self.cooldown = 0.2

    def draw(self, screen, xoff, yoff):
        draw.rect(screen, (255, 255, 255), ((self.x + xoff) * self.size, (self.y + yoff) * self.size, self.size, self.size), int(self.size/(self.size/3)))
