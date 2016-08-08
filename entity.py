from pygame import draw

class Entity:
    def __init__(self, x, y, hp, size, color):
        self.x = x
        self.y = y
        self.hp = hp
        self.size = size
        self.color = color

    def update(self, dt):
        pass

    def draw(self, screen):
        draw.rect(screen, self.color, (self.x * self.size, self.y * self.size, self.size, self.size))

class Heart(Entity):
    def __init__(self, x, y, hp, size, color):
        super().__init__(x, y, hp, size, color)

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
