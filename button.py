import arcade
import assets

class Button():

    SCALE = .5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.texture = assets.items[self.name]

    def update(self, delta):
        pass

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y,
                100, 100, arcade.color.WHITE, 0)
        #arcade.draw_scaled_texture_rectangle(self.x, self.y,
        #        self.texture, Item.SCALE, self.rotation)
