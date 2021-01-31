import arcade
import assets
import random
from datetime import datetime

class Note():

    SCALE = 1
    NOTE_IMAGE = assets.note_image
    PICTURE_IMAGE = assets.picture_image
    KALLELLSE_IMAGE = assets.kallellse_image
    KALLELLSE_WRONG_IMAGE = assets.kallellse_wrong_image
    TODAY = datetime.now().strftime("%Y-%m-%d")

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.name = "Sanic"
        self.item = "baby"
        self.date = Note.TODAY

        self.day = 1
        self.is_fake = False
        self.fake_type = None

    def update(self, delta):
        pass

    def draw(self):
        if self.day == 1:
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
        elif self.day == 2:
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
        elif self.day == 3:
            arcade.draw_scaled_texture_rectangle(
                self.x,
                self.y,
                Note.KALLELLSE_WRONG_IMAGE if self.fake_type == "Card" else Note.KALLELLSE_IMAGE,
                Note.SCALE,
                0
            )
            arcade.draw_text(
                self.name.replace("_", " ").capitalize(),
                self.x - 33,
                self.y + 58,
                arcade.color.BLACK,
                22,
                align="center", anchor_x="center", anchor_y="center",
                font_name="res/font/Note_this.ttf",
                rotation=5
            )
            item = self.item.replace("_", " ")
            if item.startswith("balloon"):
                item = " ".join(item.split()[::-1])
            arcade.draw_text(
                item,
                self.x,
                self.y - 10,
                arcade.color.BLACK,
                32,
                align="center", anchor_x="center", anchor_y="center",
                font_name="res/font/Note_this.ttf",
                rotation=5
            )
            arcade.draw_text(
                self.date,
                self.x + 200,
                self.y - 60,
                arcade.color.BLACK,
                28,
                align="center", anchor_x="center", anchor_y="center",
                font_name="res/font/Note_this.ttf",
                rotation=7
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

    def set_person_name(self, name):
        self.name = name

    def randomize_fake(self):
        """ Make sure all fields are correct before calling this function """
        self.date = Note.TODAY

        self.is_fake = random.random() < .3 and self.day == 3
        if self.is_fake:
            self.fake_type = ["Card", "Name", "Item", "Date"][random.randint(0, 3)]
            if self.fake_type == "Name":
                name = self.name
                while self.name == name:
                    name = random.choice(list(assets.persons))
                self.name = name
            elif self.fake_type == "Item":
                item = self.item
                while self.item == item:
                    item = random.choice(list(assets.items))
                self.item = item
            elif self.fake_type == "Date":
                self.date = "{}-{}-{}".format(
                    random.randint(2000, 2020),
                    random.randint(1, 12),
                    random.randint(1, 28)
                )
