import arcade
import assets
import math
import random

class IdCard():
    """
    Container and checker of validity.
    """

    def __init__(self, person, date, false_id):


        self.false_id = false_id
        incorrect_elem = 9

        if false_id:
            incorrect_elem = random.randint(0,5)

        self.person = person
        self.date = date

        if incorrect_elem == 0:
            pass
        else:
            pass

        self.texture = None
        self.name = "temp"
        self.birthdate = "01-12-2021"
        self.exp_date = "01-12-2021"
        self.iss_city = "Malmo"
        self.watermark = None
        self.gender = random.choice(["Boi","Grill","Microwave","Wolf"])


    def draw(self):
        arcade.draw_text("Name", 10, 10, arcade.color.BLACK)

    def is_valid(self):
        return self.false_id
