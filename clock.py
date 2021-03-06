import arcade
import assets

class Clock():

    SCALE = 1
    DAY_TIME = 90

    START_TIME = 8 * 60
    HOURS = 17 - 8


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = 0
        self.texture = assets.clock_image

    def update(self, delta):
        self.time += delta

    def draw(self):
        arcade.draw_scaled_texture_rectangle(
            self.x,
            self.y,
            self.texture,
            Clock.SCALE,
            0
        )
        arcade.draw_text(
            self.time_as_str(),
            self.x,
            self.y,
            arcade.color.RED,
            40,
            align="center",
            anchor_x="center",
            anchor_y="center",
            font_name="res/font/DIGITALDREAMNARROW.ttf"
        )

    def is_completed(self):
        return self.time > Clock.DAY_TIME

    def time_as_str(self):
        return "{:02}:{:02}".format(8 + int(self.time / Clock.DAY_TIME * Clock.HOURS),
                                    int(self.time / Clock.DAY_TIME * Clock.HOURS * 60 // 30 * 30) % 60)
