import random
from pygame import draw
from entity import *
from tile import Tile
from game_clock import Clock

import math

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
        self.game_clock = Clock(6, 0, 90, 6)
        self.brightness_layer = 1.0
        self.game_start = True
        self.tiles = {
            'sand' : Tile((0,0), "Sand", (244, 219, 168), self.tile_size),
            'wall' : Tile((0,0), "Wall", (60, 50, 33), self.tile_size, False, True)
            }

    def create_tile(self, x, y, tile_name):

        tile = None

        if tile_name == "Wall":
            tile = Tile((x, y), "Wall", (60, 50, 33), self.tile_size, False, True)
        else:
            tile = Tile((x, y), "Sand", (244, 219, 168), self.tile_size)

        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = tile

    def break_tile(self, x, y):
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = Tile((x, y), "Rubble", (146, 133, 108), self.tile_size)

    def spawn_entities(self):
        self.entities.append(Heart(self.map_size/2, self.map_size/2, 10, self.tile_size, (255, 0, 0)))
        self.entity_map[int((self.map_size * self.map_size)/2)] = self.entities[0]

    def spawn_monster(self):
        # Spawn area
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
                self.terrain_map[x + y * self.map_size] = Tile((x,y), "Sand", (244, 219, 168), self.tile_size)

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
            for x in range(self.map_size):
                xp = x + int(xoff)
                tile = self.terrain_map[x + y * self.map_size]
                tile.change_brightness(self.brightness_layer)
                if tile.light_source:
                    for yp in range(y-3, y+4):
                        for xp in range(x-3, x+4):
                            tile_l = self.terrain_map[xp + yp * self.map_size]
                            vx = tile.x - tile_l.x
                            vy = tile.y - tile_l.y
                            distance = math.sqrt(vx*vx + vy*vy)
                            light_amount = 1 - distance/4
                            if light_amount < 0:
                                light_amount = 0
                            tile_l.add_light(light_amount)
                else:
                    tile.emit_light = 0
                tile.draw(screen, xoff, yoff)
                if yp < 0 or yp >= self.map_size or xp < 0 or xp >= self.map_size:
                    continue

        if len(self.entities) > 0:
            for entity in self.entities:
                entity.draw(screen, xoff, yoff)
        for monster in self.monsters:
            monster.draw(screen, xoff, yoff)
