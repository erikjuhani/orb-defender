import random
from pygame import *
from entity import *
from tile import Tile
from game_clock import Clock
from sprite import *

import math

class Level:
    def __init__(self, map_size, tile_size, tiles):
        self.map_size = map_size
        self.tile_size = tile_size
        self.tiles = tiles
        self.terrain_map = [0] * (self.map_size * self.map_size) # init empty map
        self.heart_pos = 0
        self.heart_hp = 20
        self.entities = []
        self.monsters = []
        self.bullets = []
        self.generate_level()
        self.game_clock = Clock(6, 0, 40, 6)
        self.brightness_layer = 1.0
        self.game_start = True
        self.gold = 20

    def create_tile(self, x, y, tile_name):

        tile = None

        if tile_name == 'Tower':
            tile = Tile('Tower', (60, 100, 33), self.tile_size, 4, False, Sprite('img/tower.png'), False, 4)
            self.gold -= 4
        elif tile_name == 'Wall':
            tile = Tile('Wall', (60, 50, 33), self.tile_size, 20, False, Sprite('img/wall.png'), False, 2)
            self.gold -= 2
        elif tile_name == 'Torch':
            tile = Tile('Torch', (255, 255, 255), self.tile_size, 2, False, Sprite('img/torch.png'), True, 1)
            self.gold -= 1
        else:
            tile = Tile('Sand', (244, 219, 168), self.tile_size)

        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = tile

    def break_tile(self, x, y):
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = Tile("Rubble", (146, 133, 108), self.tile_size)

    def spawn_entities(self):
        x = int(self.map_size/2)
        y = int(self.map_size/2)
        self.heart_pos = (x, y)
        map_pos = x + y * self.map_size
        self.terrain_map[map_pos] = Tile('Heart', (255, 0, 0), self.tile_size, self.heart_hp, False, orb, True)

    def spawn_monster(self):
        # Spawn area
        spawn_area = [-1, self.map_size + 1]

        amount = (self.game_clock.days + 1)

        if self.game_clock.days % 5 == 0:
            amount += self.game_clock.days * 2

        for i in range(amount + 100):

            randx = random.randint(-1, self.map_size + 1)
            randy = 0

            if randx > 0 and randx < self.map_size + 1:
                randy = random.choice(spawn_area)
            else:
                randy = random.randint(-1, self.map_size + 1)

            monster = Monster(randx, randy, random.randint(3, 10), 10, self.tile_size, (114, 127, 79), 1)
            self.monsters.append(monster)

    def generate_level(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.terrain_map[x + y * self.map_size] = Tile('Sand', (244, 219, 168), self.tile_size)

        self.spawn_entities()

    def light_tile(self, ox, oy):
        for y in range(oy-6, oy+7):
            for x in range(ox-6, ox+7):
                if x >= 0 and x < self.map_size and y >= 0 and y < self.map_size:
                    map_pos = x + y * self.map_size
                    tile_l = self.terrain_map[map_pos]
                    vx = ox - x
                    vy = oy - y
                    distance = math.sqrt(vx*vx + vy*vy)
                    light_amount = 1 - distance/7
                    if distance <= 1:
                        light_amount += 0.3
                    elif distance <= 2 and distance > 1:
                        light_amount += 0.2
                    elif distance <= 3 and distance > 2:
                        light_amount += 0.1
                    elif distance <= 4 and distance > 3:
                        light_amount += 0.05
                    if light_amount < 0:
                        light_amount = 0
                    tile_l.add_light(light_amount)

    def update(self, dt):

        for y in range(self.map_size):
            for x in range(self.map_size):
                map_pos = x + y * self.map_size
                tile = self.terrain_map[map_pos]

                if not tile.passable:
                    tile.attack(x, y, self, self.monsters, dt)
                    if tile.hp <= 0:
                        self.break_tile(x, y)

                if tile.tile_name == 'Heart' and self.heart_hp > tile.hp:
                    self.heart_hp = tile.hp

                if not tile.sprite == None:
                    tile.change_img_brightness(self.brightness_layer)
                else:
                    tile.change_brightness(self.brightness_layer)

                if tile.light_source:
                    self.light_tile(x, y)
                else:
                    tile.emit_light = 0
                tile.update(dt)

        self.game_clock.tick(dt)

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
                if monster.hp == 0:
                    self.monsters.remove(monster)
                    self.gold += 2
                    continue
                monster.take_dmg(self.bullets)
                monster.simple_move(self, self.heart_pos[0], self.heart_pos[1], dt)

        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(dt)
                x = bullet.x
                y = bullet.y
                if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
                    self.bullets.remove(bullet)
                    continue

    def draw(self, screen, xoff, yoff):
        for y in range(self.map_size):
            yp = y + int(yoff)
            for x in range(self.map_size):
                xp = x + int(xoff)
                map_pos = x + y * self.map_size
                tile = self.terrain_map[map_pos]
                if yp < 0 or yp >= self.map_size or xp < 0 or xp >= self.map_size:
                    continue
                tile.draw(screen, x, y, xoff, yoff)

        if len(self.bullets) > 0:
            for bullet in self.bullets:
                x = bullet.x + xoff
                y = bullet.y + yoff
                if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
                    continue
                bullet.draw(screen, xoff, yoff)


        if len(self.entities) > 0:
            for entity in self.entities:
                entity.draw(screen, xoff, yoff)

        for monster in self.monsters:
            monster_pos = monster.x + monster.y * self.map_size
            x = monster.x + xoff
            y = monster.y + yoff
            if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
                continue
            if monster_pos > 0 and monster_pos < (self.map_size * self.map_size):
                monster.change_brightness(self.brightness_layer)
                if self.terrain_map[monster_pos].emit_light == 0:
                    monster.emit_light = 0
                else:
                    monster.emit_light = self.terrain_map[monster_pos].emit_light
                monster.draw(screen, xoff, yoff)
