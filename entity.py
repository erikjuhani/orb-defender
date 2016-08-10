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
        self.brain = Brain()

class Brain:
    def __init__(self):
        pass

    def find_path(self, target, start):
        pass

    def move(self, target):
        pass

    def attack(self, object):
        pass
