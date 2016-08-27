from pygame import draw

import math

class Bullet:
    def __init__(self, targetx, targety, x, y, speed, melee, size):
        self.speed = speed
        self.x = x + 0.5
        self.y = y + 0.5
        self.tx = targetx
        self.ty = targety
        self.size = size
        self.dir_x = 0
        self.dir_y = 0
        self.calc_movement()
        self.distance = 0
        self.dmg = 2
        self.melee = melee

    def calc_movement(self):
        xv = self.tx - self.x
        yv = self.ty - self.y
        self.distance = math.sqrt(xv*xv + yv*yv)
        self.dir_x = xv/self.distance
        self.dir_y = yv/self.distance

    def update(self, dt):
        self.x += self.dir_x * self.speed * dt
        self.y += self.dir_y * self.speed * dt

    def draw(self, screen, xoff, yoff):
        draw.ellipse(screen, (0, 0, 0), ((self.x+xoff) * self.size, (self.y+yoff) * self.size, self.size/2-1, self.size/2-1))
