from pygame import draw

class Entity:
    def __init__(self, x, y, hp, size, color):
        self.x = int(x)
        self.y = int(y)
        self.hp = hp
        self.full_hp = hp
        self.size = size
        self.color = color
        self.origc = color
        self.emit_light = 0

    def add_light(self, amount):
        if self.emit_light < 1:
            self.emit_light += amount

    def change_brightness(self, amount, tint=None):

        amount = amount + self.emit_light

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

        self.color = (r, g, b)

    def update(self, dt):
        pass

    def draw(self, screen, xoff, yoff):
        draw.rect(screen, self.color, ((self.x + xoff) * self.size, (self.y + yoff) * self.size, self.size, self.size))

class Heart(Entity):
    def __init__(self, x, y, hp, size, color):
        super().__init__(x, y, hp, size, color)
        self.passable = False

class Monster(Entity):
    def __init__(self, x, y, speed, hp, size, color, attack):
        super(self.__class__, self).__init__(x, y, hp, size, color)
        self.speed = speed
        self.attack = attack
        self.cooldown = 0
        self.dmg = 2
        self.brain = Brain()

    def check_wall(self, level, locx, locy):
        if locx >= 0 and locx < level.map_size and locy >= 0 and locy < level.map_size:
            if not level.terrain_map[locx + locy * level.map_size].passable:
                return False
        return True

    def do_attack(self, level, locx, locy, dt):
        level.terrain_map[locx + locy * level.map_size].take_dmg(self.dmg)

    def take_dmg(self, bullets):
        dmg = 0

        for bullet in bullets:
            if int(bullet.x) >= int(self.x - 0.5) and int(bullet.x) <= int(self.x + 0.5) and int(bullet.y) >= int(self.y - 0.5) and int(bullet.y) <= int(self.y - 0.5):
                dmg = bullet.dmg
                bullets.remove(bullet)
                continue

        if dmg > 0:
            self.hp -= dmg

            r = self.origc[0]
            g = self.origc[1]
            b = self.origc[2]

            r *= 1-dmg/self.full_hp
            g *= 1-dmg/self.full_hp
            b *= 1-dmg/self.full_hp

            self.origc = (r , g, b)

    def update(self, dt):
        pass

    def simple_move(self, level, targetx, targety, dt):
        self.cooldown -= 1 * (self.speed/10) * dt

        if self.cooldown < 0:
            self.cooldown = 0

        if self.cooldown == 0:
            if targetx > self.x:
                if self.check_wall(level, self.x+1, self.y):
                    self.x += 1
                else:
                    self.do_attack(level, self.x+1, self.y, dt)
                self.cooldown = 1
            elif targetx < self.x:
                if self.check_wall(level, self.x-1, self.y):
                    self.x -= 1
                else:
                    self.do_attack(level, self.x-1, self.y, dt)
                self.cooldown = 1
            if targety > self.y:
                if self.check_wall(level, self.x, self.y+1):
                    self.y += 1
                else:
                    self.do_attack(level, self.x, self.y+1, dt)
                self.cooldown = 1
            elif targety < self.y:
                if self.check_wall(level, self.x, self.y-1):
                    self.y -= 1
                else:
                    self.do_attack(level, self.x, self.y-1, dt)
                self.cooldown = 1

class Brain:
    def __init__(self):
        pass

    def find_path(self, target, start):
        pass

    def move(self, target):
        pass

    def attack(self, object):
        pass
