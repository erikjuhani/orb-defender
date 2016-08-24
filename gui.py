from pygame import draw, font
from key_dict import *

BLUE = (84, 188, 236)
WHITE = (255, 255, 255)

class Main_menu:
    def __init__(self, size):
        self.menu_state = 0 # 0 = new game, 1 = help, 2 = quit game
        self.game_state = False
        self.help_state = False

        self.new_game_color = BLUE
        self.help_color = WHITE
        self.quit_color = WHITE

        self.size = size
        self.font = font.Font(None, size)

        self.cooldown = 0
    def update(self, game, keys, dt):

        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        for key in KEY_DICT:
            if keys[key] and self.cooldown == 0:
                if KEY_DICT[key] == 'down':
                    self.menu_state += 1
                    if self.menu_state > 2:
                        self.menu_state = 0
                if KEY_DICT[key] == 'up':
                    self.menu_state -= 1
                    if self.menu_state < 0:
                        self.menu_state = 2
                if KEY_DICT[key] == 'action':
                    if self.menu_state == 0:
                        self.game_state = True
                    elif self.menu_state == 1:
                        self.help_state = True
                    elif self.menu_state == 2:
                        game.running = False
                if KEY_DICT[key] == 'escape':
                    self.help_state = False
                self.cooldown = 0.2

    def draw_help(self, screen):
        wall_of_text = 'Help!\nControls: WASD\nWhat to do: Survive:)'

        help_text = wall_of_text.split('\n')
        i = 0

        for line in help_text:
            screen.blit(self.font.render(str(line), 2, WHITE), (self.size*4, self.size*(2+i)))
            i += 1

    def draw_msg(self, msg, state):
        color = WHITE
        if state:
            color = BLUE
        return self.font.render(str(msg), 2, color)

    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), screen.get_height()))
        if self.help_state:
            self.draw_help(screen)
        else:
            screen.blit(self.draw_msg('Orb Defender', False), (self.size*4, self.size))
            screen.blit(self.draw_msg('New Game', self.menu_state == 0), (self.size*3, self.size*4))
            screen.blit(self.draw_msg('Help', self.menu_state == 1), (self.size*3, self.size*5))
            screen.blit(self.draw_msg('Quit Game', self.menu_state == 2), (self.size*3, self.size*6))

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

    def update(self, menu, cursor, keys, level, dt):
        for key in KEY_DICT:
            if keys[key]:
                if KEY_DICT[key] == 'switch':
                    self.block += 1
                    if self.block > 2:
                        self.block = 0
                if KEY_DICT[key] == 'pause':
                    self.paused = not self.paused
                if KEY_DICT[key] == 'switch' and level.heart_hp <= 0:
                    level.restart_level()
                    cursor.x = int(level.map_size/2)
                    cursor.y = int(level.map_size/2)
                if KEY_DICT[key] == 'escape' and self.paused:
                    level.restart_level()
                    cursor.x = int(level.map_size/2)
                    cursor.y = int(level.map_size/2)
                    menu.game_state = False
                    self.paused = False

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
            restart_msg = 'Press R to restart or Q to return to menu'
            screen.blit(self.draw_msg(lost_msg), (self.size*5 - len(lost_msg), self.height/2))
            screen.blit(self.draw_msg(restart_msg), (self.width/2 - len(lost_msg), self.height/2+self.size))

        #if self.show_day:
        #    screen.blit(self.font.render("Day: 1", 1, (255, 255, 255)), (self.x + self.width/2, self.y + self.size))
