import arcade
import assets

class Note():

    SCALE = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.texture = assets.note_image
        self.text = "text"

    def update(self, delta):
        pass

    def draw(self):
        arcade.draw_scaled_texture_rectangle(
            self.x,
            self.y,
            self.texture,
            Note.SCALE,
            0
        )
        arcade.draw_text(
            self.text,
            self.x - 40,
            self.y,
            arcade.color.BLACK,
            50,
            align="center",
            anchor_x="center",
            anchor_y="center",
            font_name="res/font/Note_this.ttf"
        )

    def set_text(self, text):
        if len(text.split()) % 2 == 1:
            e = [""]
        else:
            e = []

        self.text = "\n".join(
            [t1 + " " + t2 for t1, t2 in zip(text.split()[::2], text.split()[1::2] + e)]
        )
