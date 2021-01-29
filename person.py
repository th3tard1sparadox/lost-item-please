import arcade
import assets
import random

def clamp(low, v, high):
    return min(max(v, low), high)

class Person():

    MAX_ROTATION_VEL = 600
    MAX_VEL = 500

    def __init__(self, x, y, r=0):
        self.x = x
        self.vx = 0

        self.y = y
        self.vy = 0

        self.rotation = r
        self.vr = 0

        self.goal_x = None
        self.goal_y = None
        self.is_traveling = False

        self.name = random.choice(list(assets.persons))
        self.texture = assets.persons[self.name]

    def update(self, delta):
        if not self.is_traveling:
            if self.rotation % 360 > self.vr * delta:
                self.vr = Person.MAX_ROTATION_VEL
                self.rotation += delta * self.vr
            else:
                self.vr = 0
                self.rotation = 0
            return

        dx, dy = self.goal_x - self.x, self.goal_y - self.y
        l = (dx**2 + dy**2)**.5

        if l < Person.MAX_VEL * delta:
            self.x = self.goal_x
            self.y = self.goal_y
            self.vx = 0
            self.vy = 0
            self.is_traveling = False
            return

        dx /= l
        dy /= l

        speed = (self.vx**2 + self.vy**2)**.5
        if speed < Person.MAX_VEL:
            self.vx += dx * delta * Person.MAX_VEL
            self.vy += dy * delta * Person.MAX_VEL

        if self.vr < Person.MAX_ROTATION_VEL:
            self.vr += delta * Person.MAX_ROTATION_VEL

        self.x += delta * self.vx
        self.y += delta * self.vy
        self.rotation += delta * self.vr

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.x, self.y,
                self.texture, 1, self.rotation)

    def travel_to(self, x, y):
        self.is_traveling = True
        self.goal_x = x
        self.goal_y = y
        self.vx = 0
        self.vy = 0
        self.vr = 0
