from pygame import *
from level import *
from cursor import *
from camera import Camera
from gui import *

''' Game configs '''
SCALE = 4   # Scalar, which determines how the game is scaled. Basicly it's a multiplier.
FPS = 30    # Frames per second
TILE_SIZE = 8 * SCALE # Changes how big are the elements in the game world.
MAP_SIZE = 32 # Determines the size of the playable map area. min 20. Odd numbers prefered.
TILES = {'sand' : Tile('Sand', (244, 219, 168), TILE_SIZE),
         'wall' : ("Wall", (60, 50, 33), TILE_SIZE, False, True)}

class Game:
    def __init__(self):
        self.screen = display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = time.Clock()
        self.keys = key.get_pressed()
        self.level = Level(MAP_SIZE, TILE_SIZE, TILES)
        self.level.generate_level()
        self.running = True
        self.cursor = Cursor(MAP_SIZE/2, MAP_SIZE/2, TILE_SIZE)
        self.camera = Camera(self.screen_rect, TILE_SIZE, self.cursor.x, self.cursor.y)
        self.gui = Game_gui(self.screen, self.level, TILE_SIZE)

    def event_loop(self):
        for e in event.get():
            if e.type == QUIT:
                self.running = False
            elif e.type in (KEYDOWN, KEYUP):
                self.keys = key.get_pressed()

    def update(self, dt):
        self.gui.update(self.cursor, self.keys, self.level, dt)
        if not self.gui.paused and self.level.heart_hp > 0:
            self.level.update(dt)
            self.cursor.update(self.keys, self.level, dt)
            self.camera.update(self.cursor.x, self.cursor.y, self.level)

    def render(self):
        self.level.draw(self.screen, self.camera.x, self.camera.y)
        self.cursor.draw(self.screen, self.camera.x, self.camera.y)
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
