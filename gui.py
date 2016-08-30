from pygame import draw, font
from key_dict import *
from sprite import *

BLUE = (84, 188, 236)
WHITE = (255, 255, 255)

TXT_SURF = {
        'Title' : convert_string('Orb Defender'),
        'New'   : convert_string('New Game'),
        'Help'  : convert_string('Help'),
        'Quit'  : convert_string('Quit Game')
        }

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
        self.menu = {
                'Title' : transform.scale(TXT_SURF['Title'], (TXT_SURF['Title'].get_width()*6, TXT_SURF['Title'].get_height()*6)),
                'New'   : transform.scale(TXT_SURF['New'], (TXT_SURF['New'].get_width()*3, TXT_SURF['New'].get_height()*3)),
                'Help'  : transform.scale(TXT_SURF['Help'], (TXT_SURF['Help'].get_width()*3, TXT_SURF['Help'].get_height()*3)),
                'Quit'  : transform.scale(TXT_SURF['Quit'], (TXT_SURF['Quit'].get_width()*3, TXT_SURF['Quit'].get_height()*3))
                }
        change_color(self.menu['New'], self.menu_state == 0)
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

                change_color(self.menu['New'], self.menu_state == 0)
                change_color(self.menu['Help'], self.menu_state == 1)
                change_color(self.menu['Quit'], self.menu_state == 2)


    def draw_help(self, screen):
        wall_of_text = 'Help!\nControls: WASD\nWhat to do: Survive:)'
        help_text = wall_of_text.split('\n')
        width = len(wall_of_text)
        height = len(help_text)
        help_surf = Surface((width, height))
        i = 0

        for line in help_text:
            line_surf = convert_string(line)
            screen.blit(transform.scale(line_surf, (line_surf.get_width()*3, line_surf.get_height()*3)), (self.size*4, self.size*(2+i)))
            i += 1

    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), screen.get_height()))
        if self.help_state:
            self.draw_help(screen)
        else:
            screen.blit(self.menu['Title'], (self.size*2, self.size))
            screen.blit(self.menu['New'], (self.size*6, self.size*4))
            screen.blit(self.menu['Help'], (self.size*7, self.size*5))
            screen.blit(self.menu['Quit'], (self.size*6, self.size*6))

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
        self.blocks = {
                        'Wall' : transform.scale(textures['wall'],(textures['wall'].get_width()*3, textures['wall'].get_height()*3)),
                        'Tower': transform.scale(textures['tower1'],(textures['tower1'].get_width()*3, textures['tower1'].get_height()*3)),
                        'Air tower' : transform.scale(textures['tower2'],(textures['tower2'].get_width()*3, textures['tower2'].get_height()*3)),
                        'Torch' : transform.scale(textures['torch'],(textures['torch'].get_width()*3, textures['torch'].get_height()*3)),
                    }
        self.current_block = self.blocks['Wall']
        self.cooldown = 0
        self.splash = 0
        self.splash_msg = ''
        self.days = level.game_clock.days

    def change_block(self):
        pass

    def identifier(self, cx, cy, monsters):
        self.current_i = self.level.terrain_map[cx + cy * self.level.map_size].tile_name
        if len(monsters) > 0:
            for m in monsters:
                if cx == m.x and cy == m.y:
                    self.current_i = 'Monster'

    def draw_msg(self, msg):
        msg_surf = convert_string(str(msg))
        return transform.scale(msg_surf, (msg_surf.get_width()*3, msg_surf.get_height()*3))

    def draw_splash(self, msg):
        self.splash = 6
        self.splash_msg = msg

    def update(self, menu, cursor, keys, level, dt):

        if self.cooldown > 0:
            self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        if self.splash > 0:
            self.splash -= 1 * dt
        if self.splash < 0:
            self.splash = 0

        for key in KEY_DICT:
            if keys[key] and self.cooldown == 0:
                if KEY_DICT[key] == 'switch':
                    self.block += 1
                    if self.block > 2:
                        self.block = 0
                if KEY_DICT[key] == 'pause':
                    self.paused = not self.paused
                if KEY_DICT[key] == 'switch' and level.heart_hp <= 0:
                    level.restart_level()
                    cursor.x = level.map_size//2
                    cursor.y = level.map_size//2
                if KEY_DICT[key] == 'escape' and self.paused:
                    level.restart_level()
                    cursor.x = level.map_size//2
                    cursor.y = level.map_size//2
                    menu.game_state = False
                    self.paused = False
                self.cooldown = 0.2

        self.identifier(cursor.x, cursor.y, level.monsters)
        if level.gold < self.gold or level.gold > self.gold:
            self.gold = level.gold
        self.current_block = self.blocks[cursor.menu_block[cursor.block]]

        if (level.game_clock.days > self.days or level.game_start) and level.game_clock.hours == 8:
            self.draw_splash('DAWN ' + str(level.game_clock.days))
            self.days = level.game_clock.days

    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), (0, 0, self.width, self.size))
        screen.blit(self.current_block, (self.width-self.size*2, self.y, self.size, self.size))
        draw.ellipse(screen, (255, 255, 0), (self.size//3, self.y+self.size//3-1, self.size//2-1, self.size//2-1))
        screen.blit(self.draw_msg(self.gold), (self.size, self.size//4))
        screen.blit(self.draw_msg(self.current_i), (self.size*4, self.size//4))
        screen.blit(self.draw_msg(self.level.heart_hp), (self.size*8, self.size//4))
        if self.paused:
            screen.blit(self.draw_msg('GAME PAUSED'), (self.size*8, self.size//4))

        if self.splash > 0:
            screen.blit(self.draw_msg(self.splash_msg), (self.size*7, self.size*2))

        if self.level.heart_hp <= 0:
            lost_msg = 'Your kingdom has fallen on:'
            day_msg = 'DAY:' + str(self.level.game_clock.days)
            restart_msg1 = 'Press R to restart'
            restart_msg2 = 'Press Q to return to menu'
            screen.blit(self.draw_msg(lost_msg), (self.size*2, self.size*3))
            screen.blit(self.draw_msg(day_msg), (self.size*7, self.size*4))
            screen.blit(self.draw_msg(restart_msg1), (self.size*4, self.size*5))
            screen.blit(self.draw_msg(restart_msg2), (self.size*3, self.size*6))
