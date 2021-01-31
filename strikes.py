import arcade
import assets

class Strikes():

    SCALE = 1
    BOX_WIDTH = 90
    STRIKE_IMAGE = assets.strike_image
    NOT_STRIKE_IMAGE = assets.not_strike_image

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.strikes = 0

    def update(self, delta):
        pass

    def draw(self):

        for i in range(3):
            arcade.draw_scaled_texture_rectangle(
                self.x + (i - 1) * Strikes.BOX_WIDTH,
                self.y,
                Strikes.STRIKE_IMAGE if i < self.strikes else Strikes.NOT_STRIKE_IMAGE,
                Strikes.SCALE,
                0
            )
