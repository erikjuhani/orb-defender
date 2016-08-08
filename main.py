import pygame
import sys
from level import *
from cursor import *

CAPTION = "The Fortress Heart"
WIDTH = 640
HEIGHT = 480
SCALE = 4
SCREEN_SIZE = (WIDTH, HEIGHT)

class Gui:
    def __init__(self):
        pass

class Menu:
    def __init__(self):
        pass

    def switch(self):
        pass

    def start(self):
        pass




class Heart:
    def __init__(self, x, y, hp, size):
        self.x = x
        self.y = y
        self.hp = hp
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        self.keys = pygame.key.get_pressed()
        self.size = 8 * SCALE
        self.heart = Heart(WIDTH/2, HEIGHT/2, 100, self.size)

        self.level = Level(20, self.size)
        self.level.generate_level()
        self.cursor = Cursor(10, 10, self.size)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.keys = pygame.key.get_pressed()

    def update(self, dt):
        self.level.update(dt)
        self.cursor.update(self.keys, self.level, dt)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.level.draw(self.screen)
        self.cursor.draw(self.screen)
        pygame.display.update()

    def game_loop(self):
        dt = 0
        self.clock.tick(self.fps)
        while self.running:

            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(self.fps)/1000.0

def main():

    pygame.init()
    pygame.display.set_caption(CAPTION)
    pygame.display.set_mode(SCREEN_SIZE)
    Game().game_loop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
