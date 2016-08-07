import pygame
import sys

CAPTION = "The Fortress Heart"
WIDTH = 640
HEIGHT = 480
SCALE = 4
SCREEN_SIZE = (WIDTH, HEIGHT)

KEY_DICT = {pygame.K_a : 'left',
            pygame.K_d : 'right',
            pygame.K_w : 'up',
            pygame.K_s : 'down',
            pygame.K_e : 'action'}

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

class Cursor:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.draw_x = self.x
        self.draw_y = self.y
        self.speed = 1
        self.cooldown = 0

    def update(self, keys, dt):
        self.cooldown -= 1 * dt
        if self.cooldown < 0:
            self.cooldown = 0

        for key in KEY_DICT:
            if keys[key] and self.cooldown == 0:
                print(KEY_DICT[key])
                if KEY_DICT[key] == 'left':
                    self.x -= self.speed
                    self.draw_x -= self.speed * self.size
                if KEY_DICT[key] == 'right':
                    self.x += self.speed
                    self.draw_x += self.speed * self.size
                if KEY_DICT[key] == 'up':
                    self.y -= self.speed
                    self.draw_y -= self.speed * self.size
                if KEY_DICT[key] == 'down':
                    self.y += self.speed
                    self.draw_y += self.speed * self.size
                if KEY_DICT[key] == 'action':
                    pass
                self.cooldown = 0.2

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.draw_x, self.draw_y, self.size, self.size), 1)


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
        self.cursor = Cursor(WIDTH/2, HEIGHT/2, self.size)
        self.heart = Heart(WIDTH/2, HEIGHT/2, 100, self.size)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.keys = pygame.key.get_pressed()

    def update(self, dt):
        self.cursor.update(self.keys, dt)

    def render(self):
        self.screen.fill((255, 255, 255))
        self.heart.draw(self.screen)
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
