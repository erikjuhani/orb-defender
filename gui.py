from pygame import draw, font
from key_dict import *

class Main_menu:
    def __init__(self):
        self.menu_state = 0 # 0 = new game, 1 = 'load', 2 = help, 3 = quit game
        self.game_state = False
    def update(self, keys, dt):
        pass

class Inventory:
    def __init__(self):
        pass

class Game_gui:
    def __init__(self, screen, level, size):
        self.x = 0
        self.y = 0
        self.font = font.Font(None, size)
        self.current_i = 'Nothing'
        self.size = size
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.level = level
        self.block = 0
        self.gold = level.gold
        self.paused = False
        self.current_block = (0, 0, 0)

    def change_block(self):
        pass

    def identifier(self, cx, cy, monsters):
        self.current_i = self.level.terrain_map[cx + cy * self.level.map_size].tile_name
        if len(monsters) > 0:
            for m in monsters:
                if cx == m.x and cy == m.y:
                    self.current_i = 'Monster'

    def draw_msg(self, msg):
        return self.font.render(str(msg), 1, (255, 255, 255))

    def update(self, cursor, keys, level, dt):
        for key in KEY_DICT:
            if keys[key]:
                if KEY_DICT[key] == 'switch':
                    self.block += 1
                    if self.block > 2:
                        self.block = 0
                if KEY_DICT[key] == 'pause':
                    self.paused = not self.paused
        self.identifier(cursor.x, cursor.y, level.monsters)
        if level.gold < self.gold or level.gold > self.gold:
            self.gold = level.gold
        if cursor.menu_block[cursor.block] == 'Wall':
            self.current_block = (60, 50, 33)
        elif cursor.menu_block[cursor.block] == 'Tower':
            self.current_block = (60, 100, 33)
        elif cursor.menu_block[cursor.block] == 'Torch':
            self.current_block = (255, 255, 255)


    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.size))
        draw.rect(screen, self.current_block, (self.width-self.size*2, self.y, self.size, self.size))
        draw.ellipse(screen, (255, 255, 0), (self.x + self.size/3, self.y+self.size/3-1, self.size/2-1, self.size/2-1))
        screen.blit(self.draw_msg(self.gold), (self.x + self.size, self.y + self.size/5))
        screen.blit(self.draw_msg(self.current_i), (self.x + self.size*4, self.y + self.size/5))
        screen.blit(self.draw_msg(self.level.heart_hp), (self.x + self.size*8, self.y + self.size/5))
        if self.level.heart_hp <= 0:
            lost_msg = 'Your kingdom has fallen on day: ' + str(self.level.game_clock.days)
            restart_msg = 'Press R to restart'
            screen.blit(self.draw_msg(lost_msg), (self.size*5 - len(lost_msg), self.height/2))
            screen.blit(self.draw_msg(restart_msg), (self.width/2 - len(lost_msg), self.height/2+self.size))

        #if self.show_day:
        #    screen.blit(self.font.render("Day: 1", 1, (255, 255, 255)), (self.x + self.width/2, self.y + self.size))
