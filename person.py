import arcade

def clamp(low, v, high):
    return min(max(v, low), high)

class Person():

    MAX_ROTATION_VEL = 200
    MAX_VEL = 200
    SIZE = 100

    def __init__(self, x, y):
        self.x = x
        self.vx = 0

        self.y = y
        self.vy = 0

        self.rotation = 0
        self.vr = 0

        self.goal_x = None
        self.goal_y = None
        self.is_traveling = False

    def update(self, delta):
        if not self.is_traveling:
            return

        dx, dy = self.goal_x - self.x, self.goal_y - self.y
        l = (dx**2 + dy**2)**.5

        if l < 4:
            self.x = self.goal_x
            self.y = self.goal_y
            self.vx = 0
            self.vy = 0
            self.vr = 0
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
        arcade.draw_rectangle_filled(self.x, self.y,
                Person.SIZE, Person.SIZE,
                arcade.color.WHITE,
                tilt_angle=self.rotation)

    def travel_to(self, x, y):
        self.is_traveling = True
        self.goal_x = x
        self.goal_y = y
