import random
from pygame import draw

PALETTE = {'sand' : (244, 219, 168)}

class Level:
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.terrain_map = [0] * (self.map_size * self.map_size) # init empty map
        self.entity_map = self.terrain_map

        self.entities = []

    def create_tile(self, x, y, tile_name):
        tile = None
        if tile_name == "Wall":
            tile = Tile(x, y, "Wall", (0, 0, 0), self.tile_size)
        else:
            tile = Tile(x, y, "Sand", (244, 219, 168), self.tile_size)
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = tile

    def break_tile(self, x, y):
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = Tile(x, y, "Rubble", (146, 133, 108), self.tile_size)

    def generate_level(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.terrain_map[x + y * self.map_size] = Tile(x, y, "Sand", (244, 219, 168), self.tile_size)

    def update(self, dt):
        if len(self.entities) > 0:
            for entity in self.entities:
                entity.update(dt)

    def draw(self, screen):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.terrain_map[x + y * self.map_size].draw(screen)


class Tile:
    def __init__(self, x, y, tile_name, color, size, passable=True):
        self.x = x
        self.y = y
        self.tile_name = tile_name
        self.color = color
        self.size = size
        self.passable = passable

    def draw(self, screen):
        draw.rect(screen, self.color, (self.x*self.size, self.y*self.size, self.size, self.size))