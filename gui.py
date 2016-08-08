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
        self.size = size
        self.width = screen.get_width()
        self.height = self.size
        self.level = level
        self.block = 0
        self.gold = 10
        self.paused = False

    def change_block(self):
        pass

    def update(self, keys, dt):
        for key in KEY_DICT:
            if keys[key]:
                if KEY_DICT[key] == 'switch':
                    self.block += 1
                    if self.block > 2:
                        self.block = 0
                if KEY_DICT[key] == 'pause':
                    self.paused = not self.paused

    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        draw.ellipse(screen, (255, 255, 0), (self.x + self.size/3, self.y+self.size/3-1, self.size/2-1, self.size/2-1))
        screen.blit(self.font.render(str(self.gold), 1, (255, 255, 255)), (self.x + self.size, self.y + self.size/5))
        #if self.show_day:
        #    screen.blit(self.font.render("Day: 1", 1, (255, 255, 255)), (self.x + self.width/2, self.y + self.size))
