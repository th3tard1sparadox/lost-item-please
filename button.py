import arcade
import assets

class Button():

    SCALE = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, delta):
        pass

    def draw(self):
        arcade.draw_scaled_texture_rectangle(
            self.x,
            self.y,
            assets.button_image,
            Button.SCALE,
            0
        )
