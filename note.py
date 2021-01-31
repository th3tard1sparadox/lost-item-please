import arcade
import assets

class Note():

    SCALE = 1
    NOTE_IMAGE = assets.note_image
    PICTURE_IMAGE = assets.picture_image

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = "baby"
        self.day = 1

    def update(self, delta):
        pass

    def draw(self):
        if self.day == 1:
            arcade.draw_scaled_texture_rectangle(
                self.x,
                self.y,
                Note.NOTE_IMAGE,
                Note.SCALE,
                0
            )
            arcade.draw_text(
                self.text,
                self.x - 50,
                self.y,
                arcade.color.BLACK,
                48,
                align="center",
                anchor_x="center",
                anchor_y="center",
                font_name="res/font/Billys_Hand_Thin.ttf"
            )
        elif self.day == 2:
            arcade.draw_scaled_texture_rectangle(
                self.x,
                self.y,
                Note.PICTURE_IMAGE,
                Note.SCALE,
                0
            )

            arcade.draw_scaled_texture_rectangle(
                self.x - 20,
                self.y + 60,
                assets.items[self.item],
                Note.SCALE * .30,
                35
            )


    def set_item(self, item):
        self.item = item
        text = assets.descriptions[item]
        if len(text.split()) % 2 == 1:
            e = [""]
        else:
            e = []

        self.text = "\n".join(
            [t1 + " " + t2 for t1, t2 in zip(text.split()[::2], text.split()[1::2] + e)]
        )
