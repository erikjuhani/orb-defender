from pygame import draw

class Entity:
    def __init__(self, x, y, hp, size, color):
        self.x = int(x)
        self.y = int(y)
        self.hp = hp
        self.size = size
        self.color = color

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
        self.brain = Brain()

    def update(self, dt):
        pass

    def simple_move(self, targetx, targety, dt):
        self.cooldown -= 1 * (self.speed/10) * dt

        if self.cooldown < 0:
            self.cooldown = 0

        if self.cooldown == 0:
            if targetx > self.x:
                self.x += 1
                self.cooldown = 1
            elif targetx < self.x:
                self.x -= 1
                self.cooldown = 1
            if targety > self.y:
                self.y += 1
                self.cooldown = 1
            elif targety < self.y:
                self.y -= 1
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
