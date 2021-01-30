import arcade
import assets

class Clock():

    SCALE = .5
    DAY_TIME = 60

    START_TIME = 8 * 60
    HOURS = 17 - 8


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        #self.texture = assets.items[self.name]

    def update(self, delta):
        self.time += delta

    def draw(self):
        arcade.draw_text(
            "{:02}:{:02}".format(8 + int(self.time / Clock.DAY_TIME* Clock.HOURS),
                                 int(self.time / Clock.DAY_TIME * Clock.HOURS * 60 // 30 * 30) % 60),
            self.x,
            self.y,
            arcade.color.RED,
            20,
            align="center"
        )
        #arcade.draw_scaled_texture_rectangle(self.x, self.y,
        #        self.texture, Item.SCALE, self.rotation)
