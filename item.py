import arcade
import assets
import random

class Item():

    SCALE = .35

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.orig_x = x
        self.orig_y = y

        self.rotation = 0

        self.name = name
        self.texture = assets.items[self.name]

    def update(self, delta):
        pass

    def draw(self):
        arcade.draw_scaled_texture_rectangle(self.x, self.y,
                self.texture, Item.SCALE, self.rotation)

    def move(self, x, y):
        self.x = x
        self.y = y

    def play_sound(self):
        if f"item_{self.name}" in assets.sounds:
            return arcade.play_sound(assets.sounds[f"item_{self.name}"])
        else:
            p = arcade.play_sound(assets.sounds["silence"])
            p.pause()
            return p
