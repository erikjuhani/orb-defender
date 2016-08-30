import random
from pygame import *
from entity import *
from tile import Tile
from game_clock import Clock
from sprite import *

import math

DEFAULT_CLOCK = 6, 0, 10, 6
FAST_CLOCK = 6, 0, 60, 6
REAL_CLOCK = 6, 0, 1, 6

class Level:
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.terrain_map = [0] * (self.map_size * self.map_size) # init empty map
        self.heart_pos = 0
        self.heart_hp = 20
        self.monsters = []
        self.bullets = []
        self.generate_level()
        self.game_clock = Clock(6, 0, 20, 6)
        self.brightness_layer = 0.0
        self.game_start = True
        self.gold = 60
        for key in textures:
            textures[key].convert()

    def restart_level(self):
        self.heart_pos = 0
        self.heart_hp = 20
        self.entities = []
        self.monsters = []
        self.bullets = []
        self.generate_level()
        self.game_clock = Clock(6, 0, 20, 6)
        self.brightness_layer = 0.0
        self.game_start = True
        self.gold = 60

    def create_tile(self, x, y, tile_name):

        tile = None

        if tile_name == 'Tower' and self.gold - 40 >= 0:
            tile = Tile(x, y, 'Tower', (244, 219, 168), self.tile_size, Sprite(textures['tower1']), 8, False, False, 40)
            self.gold -= tile.tile_price
        elif tile_name == 'Air tower' and self.gold - 10 >= 0:
            tile = Tile(x, y, 'Air tower', (244, 219, 168), self.tile_size, Sprite(textures['tower2']), 4, False, False, 10)
            self.gold -= tile.tile_price
        elif tile_name == 'Wall' and self.gold - 5 >= 0:
            tile = Tile(x, y, 'Wall', (244, 219, 168), self.tile_size, Sprite(textures['wall']), 20, False, False, 5)
            self.gold -= tile.tile_price
        elif tile_name == 'Torch' and self.gold - 2 >= 0:
            tile = Tile(x, y, 'Torch', (244, 219, 168), self.tile_size, Sprite(textures['torch']), 2, False, True, 2)
            self.gold -= tile.tile_price
        elif tile_name == 'Farm' and self.gold - 50 >= 0:
            tile = Tile(x, y, 'Farm', (244, 219, 168), self.tile_size, Sprite(textures['farm']), 10, False, False, 50)
            self.gold -= tile.tile_price
        else:
            tile = Tile(x, y, 'Sand', (244, 219, 168), self.tile_size)

        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = tile

    def break_tile(self, x, y):
        pos = (int(x + y * self.map_size))
        self.terrain_map[pos] = Tile(x, y, 'Rubble', (146, 133, 108), self.tile_size)

    def spawn_entities(self):
        x = self.map_size//2
        y = self.map_size//2
        self.heart_pos = (x, y)
        map_pos = x + y * self.map_size
        self.terrain_map[map_pos] = Tile(x, y, 'Heart', (244, 219, 168), self.tile_size, Sprite(textures['orb']), self.heart_hp, False, True)

    def spawn_monsters(self):

        amount = self.game_clock.days

        if self.game_clock.days % 10 == 0:
            amount += int(self.game_clock.days * 1.1)

        self.spawn_monster('basic', amount + 1)

        if self.game_clock.days % 15 == 0:
            self.spawn_monster('spawner', amount//10)

        if self.game_clock.days % 5 == 0:
            self.spawn_monster('crawler', amount//2)

        if self.game_clock.days % 3 == 0:
            self.spawn_monster('flyer', amount + 2)

    def spawn_monster(self, monster_type, amount):
        spawn_area = [-1, self.map_size + 1]
        monster = None

        for m in range(amount):
            randx = random.randint(-1, self.map_size + 1)
            randy = 0

            if randx > 0 and randx < self.map_size + 1:
                randy = random.choice(spawn_area)
            else:
                randy = random.randint(-1, self.map_size + 1)

            if monster_type == 'crawler':
                monster = Monster(randx, randy, random.randint(3, 4), 25, self.tile_size, (114, 127, 79), 4, False, False, Sprite(textures['monster2']))
            elif monster_type == 'flyer':
                monster = Monster(randx, randy, random.randint(8, 10), 3, self.tile_size, (114, 127, 79), 0.5, True, False, Sprite(textures['monster3']))
            elif monster_type == 'spawner':
                monster = Monster(randx, randy, random.randint(2, 4), 50, self.tile_size, (114, 127, 79), 8, False, True, Sprite(textures['monster4']))
            else:
                monster = Monster(randx, randy, random.randint(5, 7), 10, self.tile_size, (114, 127, 79), 2, False, False, Sprite(textures['monster1']))

            self.monsters.append(monster)

    def generate_level(self):
        for y in range(self.map_size):
            for x in range(self.map_size):
                self.terrain_map[x + y * self.map_size] = Tile(x, y, 'Sand', (244, 219, 168), self.tile_size)

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

        for pos in range(self.map_size * self.map_size):
            tile = self.terrain_map[pos]
            if not tile.passable:
                tile.attack(tile.x, tile.y, self, self.monsters, dt)
                if tile.hp <= 0:
                    self.break_tile(tile.x, tile.y)

            if tile.tile_name == 'Heart' and self.heart_hp > tile.hp:
                self.heart_hp = tile.hp

            if not tile.sprite == None:
                tile.change_img_brightness(self.brightness_layer)

            tile.change_brightness(self.brightness_layer)

            if tile.light_source:
                self.light_tile(tile.x, tile.y)
            else:
                tile.emit_light = 0
            tile.update(dt)

        self.game_clock.tick(dt)

        if self.game_clock.hours >= 18 or self.game_clock.hours < 6:
            self.brightness_layer += -((1 / self.game_clock.sun_delay / 60) * self.game_clock.speed) * dt
        else:
            self.brightness_layer += ((1 / self.game_clock.sun_delay / 60) * self.game_clock.speed) * dt

        if self.game_clock.hours == 9 and self.game_clock.minutes == 0:
            if self.game_clock.days < 3:
                self.gold += (self.game_clock.days-1) * 5
            else:
                self.gold += 20
            self.game_start = False

        if self.brightness_layer > 1:
            self.brightness_layer = 1
        if self.brightness_layer < 0:
            self.brightness_layer = 0

        if self.game_clock.hours == 0 and self.game_clock.minutes == 0:
            self.spawn_monsters()

        for i in range(len(self.monsters)):
            monster = self.monsters[i]

            for j in range(len(self.bullets)):
                bullet = self.bullets[j]
                dmg = 0
                collide_x = abs(bullet.x-monster.x)
                collide_y = abs(bullet.y-monster.y)
                if collide_x < 0.5 and collide_y < 0.5:
                    if bullet.melee and not monster.flyer:
                        dmg = bullet.dmg
                        self.bullets[j].remove = True
                    elif bullet.melee and monster.flyer:
                        dmg = bullet.dmg
                        self.bullets[j].remove = True
                self.monsters[i].take_dmg(dmg)

            if monster.hp <= 0:
                pos = monster.x + monster.y * self.map_size
                terrain = self.terrain_map[pos]
                if terrain.passable and not terrain.tile_name == 'Bones':
                    self.terrain_map[pos] = Tile(monster.x, monster.y, 'Bones', (244, 219, 168), self.tile_size, Sprite(textures['bones']))
                self.monsters[i].remove = True
            monster.simple_move(self, self.heart_pos[0], self.heart_pos[1], dt)

        self.monsters[:] = [monster for monster in self.monsters if not monster.remove]

        for i in range(len(self.bullets)):
            bullets = self.bullets
            bullet = bullets[i]
            bullet.update(dt)
            x = bullet.x
            y = bullet.y
            if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size or bullet.timer <= 0:
                self.bullets[i].remove = True
                continue

        self.bullets[:] = [x for x in self.bullets if not x.remove]

    def draw(self, screen, xoff, yoff):
        for pos in range(self.map_size * self.map_size):
            tile = self.terrain_map[pos]
            yp = tile.y + int(yoff)
            xp = tile.x + int(xoff)
            if yp < 0 or yp >= self.map_size or xp < 0 or xp >= self.map_size:
                continue
            tile.draw(screen, tile.x, tile.y, xoff, yoff)

        for i in range(len(self.bullets)):
            bullet = self.bullets[i]
            x = bullet.x + xoff
            y = bullet.y + yoff
            if x < 0 or x >= self.map_size or y < 0 or y >= self.map_size:
                continue
            bullet.draw(screen, xoff, yoff)

        for i in range(len(self.monsters)):
            monster = self.monsters[i]
            monster_pos = monster.x + monster.y * self.map_size
            x = monster.x + xoff
            y = monster.y + yoff
            if y < 0 or y >= self.map_size or x < 0 or x >= self.map_size:
                continue
            if monster_pos > 0 and monster_pos < (self.map_size * self.map_size):
                monster.change_img_brightness(self.brightness_layer)
                if self.terrain_map[monster_pos].emit_light == 0:
                    monster.emit_light = 0
                else:
                    monster.emit_light = self.terrain_map[monster_pos].emit_light
                monster.draw(screen, xoff, yoff)
