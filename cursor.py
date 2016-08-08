from pygame import *
from key_dict import *

menu_switch = {'Build' : True,
               'Wall'  : True}

class Cursor:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 1
        self.cooldown = 0

    def update(self, keys, level, gui, dt):

        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        for key in KEY_DICT:
            if keys[key] and self.cooldown == 0:
                if KEY_DICT[key] == 'left':
                    self.x -= self.speed
                if KEY_DICT[key] == 'right':
                    self.x += self.speed
                if KEY_DICT[key] == 'up':
                    self.y -= self.speed
                if KEY_DICT[key] == 'down':
                    self.y += self.speed
                if KEY_DICT[key] == 'switch':
                    menu_switch['Build'] = not menu_switch['Build']

                if KEY_DICT[key] == 'action':
                    if menu_switch['Build'] and menu_switch['Wall'] and gui.gold > 0:
                        if not level.terrain_map[self.x + self.y * level.map_size].tile_name == 'Wall':
                            level.create_tile(self.x, self.y, 'Wall')
                            gui.gold -= 1
                    elif not menu_switch['Build']:
                        if level.terrain_map[self.x + self.y * level.map_size].tile_name == 'Wall':
                            level.break_tile(self.x, self.y)
                            gui.gold += 1
                self.cooldown = 0.2

    def draw(self, screen):
        draw.rect(screen, (255, 255, 255), (self.x * self.size, self.y * self.size, self.size, self.size), int(self.size/(self.size/3)))
