import arcade
import assets
import random

class Item():

    SCALE = .35

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.orig_x = x
        self.orig_y = y

        self.rotation = 0

        self.name = random.choice(list(assets.items))
        self.texture = assets.items[self.name]

    def update(self, delta):
        pass

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.x, self.y,
                self.texture, Item.SCALE, self.rotation)
