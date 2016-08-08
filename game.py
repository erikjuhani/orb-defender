from pygame import *
from level import *
from cursor import *
from gui import *
from config import *

class Game:
    def __init__(self):
        self.screen = display.get_surface()
        self.clock = time.Clock()
        self.keys = key.get_pressed()
        self.level = Level(20, TILE_SIZE)
        self.level.generate_level()
        self.running = True
        self.cursor = Cursor(10, 10, TILE_SIZE)
        self.gui = Game_gui(self.screen, self.level, TILE_SIZE)

    def event_loop(self):
        for e in event.get():
            if e.type == QUIT:
                self.running = False
            elif e.type in (KEYDOWN, KEYUP):
                self.keys = key.get_pressed()

    def update(self, dt):
        self.gui.update(self.keys, dt)
        if not self.gui.paused:
            self.level.update(dt)
            self.cursor.update(self.keys, self.level, self.gui, dt)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.level.draw(self.screen)
        self.cursor.draw(self.screen)
        self.gui.draw(self.screen)
        display.update()

    def game_loop(self):
        dt = 0
        self.clock.tick(FPS)
        while self.running:
            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(FPS)/1000.0
