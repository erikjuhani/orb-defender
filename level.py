import random
from pygame import draw
from entity import *
from game_clock import Clock

class Level:
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.terrain_map = [0] * (self.map_size * self.map_size) # init empty map
        self.entity_map  = [0] * (self.map_size * self.map_size)
        self.entities = []
        self.monsters = []
        self.generate_level()
        self.spawn_entities()
        self.game_clock = Clock(6, 0, 50, 6)
        self.brightness_layer = 1.0
        self.game_start = True

    def create_tile(self, x, y, tile_name):

        tile = None

        if tile_name == "Wall":
            tile = Tile(x, y, "Wall", (60, 50, 33), self.tile_size)
        else:
            tile = Tile(x, y, "Sand", (244, 219, 168), self.tile_size)

        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = tile

    def break_tile(self, x, y):
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = Tile(x, y, "Rubble", (146, 133, 108), self.tile_size)

    def spawn_entities(self):
        self.entities.append(Heart(self.map_size/2, self.map_size/2, 10, self.tile_size, (255, 0, 0)))
        self.entity_map[int((self.map_size * self.map_size)/2)] = self.entities[0]

    def spawn_monster(self):
        # Spawn area
        # x = - 1 - map_size + 1
        spawn_area = [-1, self.map_size + 1]

        for i in range(10):

            randx = random.randint(-1, self.map_size + 1)
            randy = 0

            if randx > 0 and randx < self.map_size + 1:
                randy = random.choice(spawn_area)
            else:
                randy = random.randint(-1, self.map_size + 1)

            self.monsters.append(Monster(randx, randy, random.randint(3, 10), 10, self.tile_size, (0, 0, 0), 1))

    def generate_level(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.terrain_map[x + y * self.map_size] = Tile(x, y, "Sand", (244, 219, 168), self.tile_size)

    def update(self, dt):

        self.game_clock.tick(dt)
        print(self.game_clock)

        if self.game_clock.hours >= 18 or self.game_clock.hours < 6:
            self.brightness_layer += -((1 / self.game_clock.sun_delay / 60) * self.game_clock.speed) * dt
        else:
            self.brightness_layer += ((1 / self.game_clock.sun_delay / 60) * self.game_clock.speed) * dt

        if self.game_start and self.game_clock.hours == 6:
            self.brightness_layer = 0.0
            self.game_start = False

        if self.brightness_layer > 1:
            self.brightness_layer = 1
        if self.brightness_layer < 0:
            self.brightness_layer = 0

        if self.game_clock.hours == 0 and self.game_clock.minutes == 0:
            self.spawn_monster()

        if len(self.entities) > 0:
            for entity in self.entities:
                entity.update(dt)

        if len(self.monsters) > 0:
            for monster in self.monsters:
                monster.simple_move(self.entities[0].x, self.entities[0].y, dt)

    def draw(self, screen, xoff, yoff):
        for y in range(self.map_size):
            yp = y + int(yoff)
            if yp < 0 or yp >= self.map_size:
                continue
            for x in range(self.map_size):
                xp = x + int(xoff)
                if xp < 0 or xp >= self.map_size:
                    continue
                tile = self.terrain_map[x + y * self.map_size]
                tile.change_brightness(self.brightness_layer)
                tile.draw(screen, xoff, yoff)

        if len(self.entities) > 0:
            for entity in self.entities:
                entity.draw(screen, xoff, yoff)
        for monster in self.monsters:
            monster.draw(screen, xoff, yoff)

class Tile:
    def __init__(self, x, y, tile_name, color, size, passable=True, light_source=False):
        self.x = x
        self.y = y
        self.tile_name = tile_name
        self.color = color
        self.origc = color
        self.brightness_layer = 1.0
        self.size = size
        self.passable = passable
        self.light_source = light_source

    def change_brightness(self, amount, tint=None):
        r = self.origc[0]
        g = self.origc[1]
        b = self.origc[2]

        max_r = r
        max_g = g
        max_b = b

        min_r = r * 0.01
        min_g = g * 0.01
        min_b = b * 0.01

        r *= amount
        g *= amount
        b *= amount

        if not tint == None:
            if 'r' in tint:
                r += r * amount
            if 'g' in tint:
                g += g * amount
            if 'b' in tint:
                b += b * amount

        if r < min_r:
            r = min_r
        if g < min_g:
            g = min_g
        if b < min_b:
            b = min_b

        if r > max_r:
            r = max_r
        if g > max_g:
            g = max_g
        if b > max_b:
            b = max_b

        if not self.light_source:
            self.color = (r, g, b)

    def update(self, dt):
        pass


    def draw(self, screen, xoff, yoff):
        draw.rect(screen, self.color, ((self.x+xoff)*self.size, (self.y+yoff)*self.size, self.size, self.size))
