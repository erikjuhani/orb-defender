import pygame

CAPTION = "The Fortress Heart"
WIDTH = 640
HEIGHT = 480
SCREEN_SIZE = (WIDTH, HEIGHT)

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = True
        self.keys = pygame.key.get_pressed()
    def update(self):
        pass
    def render(self):
        pass
