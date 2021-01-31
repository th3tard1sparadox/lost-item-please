import arcade
import assets
import math
import random

class IdCard():
    """
    Container and checker of validity.
    """

    def __init__(self, person, false_id):

        """
        Init the card
        """

        self.false_id = false_id
        self.incorrect_elem = None

        self.person = person

        # Generate a set of valid elemements

        self.id_texture = assets.backgrounds["idcard"]
        self.texture = self.person.texture
        self.name = self.person.name

        self.birthdate = "{day}-{month}-{year}".format(
            day = str(random.randint(1,28)),
            month = str(random.randint(1,12)),
            year = str (random.randint(1950, 2010)))

        self.exp_date = "{day}-{month}-{year}".format(
            day = str(random.randint(1,28)),
            month = str(random.randint(1,12)),
            year = str (random.randint(2022, 2024)))

        self.iss_city = random.choice(["Malmo","Stockholm",
                                       "Goteborg","Linkoping",
                                       "Norrkoping","Koping"])

        self.gender = random.choice(["Boi","Grill","Microwave","Wolf"])

        if false_id:
            self.incorrect_elem = random.randint(0,5)
            self.invalid_element_generator()


    def draw(self):
        """
        Draw current ID-Card
        """

        self.x, self.y = 1550, 850
        self.x_to = - 70
        self.y_tos = 150

        arcade.draw_scaled_texture_rectangle(self.x, self.y, self.id_texture, 1)
        arcade.draw_scaled_texture_rectangle(self.x-235, self.y+75, self.texture, 0.4)
        arcade.draw_text("Name: " + self.name.capitalize().replace("_", " "),
                         self.x + self.x_to,
                         self.y + self.y_tos,
                         arcade.color.BLACK, 20,
                         font_name="res/font/Hand_Power.ttf")
        arcade.draw_text("Birthday: " + self.birthdate,
                         self.x + self.x_to,
                         self.y + self.y_tos -70,
                         arcade.color.BLACK, 20,
                         font_name="res/font/Hand_Power.ttf")
        arcade.draw_text("Expiration Date: " + self.exp_date,
                         self.x + self.x_to,
                         self.y + self.y_tos -155,
                         arcade.color.BLACK, 20,
                         font_name="res/font/Hand_Power.ttf")
        arcade.draw_text("Issuing City: " + self.iss_city,
                         self.x + self.x_to,
                         self.y + self.y_tos -235,
                         arcade.color.BLACK, 20,
                         font_name="res/font/Hand_Power.ttf")
        arcade.draw_text("Gender: " + self.gender,
                         self.x + self.x_to,
                         self.y + self.y_tos -310,
                         arcade.color.BLACK, 20,
                         font_name="res/font/Hand_Power.ttf")


    def is_false(self):
        """
        Check if valid
        """
        return self.false_id


    def invalidity_reason(self):
        """
        Do not call if valid
        """

        if self.incorrect_elem != None:
            reasons = ["Incorrect Watermark", "incorrect Image",
                       "Incorrect Name", "Incorrect Birthdate",
                       "Incorrect Expiration Date", "Incorrect Issuing City"]
            return reasons[self.incorrect_elem]

        return ""


    def invalid_element_generator(self):
        """
        Generate an invalid element
        """

        if   self.incorrect_elem == 0:
            self.id_texture = assets.backgrounds["idcard_wrong"]

        elif self.incorrect_elem == 1:
            name = self.name
            while self.name == name:
                name = random.choice(list(assets.persons))

            self.texture = assets.persons[name]

        elif self.incorrect_elem == 2:
            name = self.name
            while self.name == name:
                name = random.choice(list(assets.persons))

            self.name = name

        elif self.incorrect_elem == 3:
            self.birthdate = "{day}-{month}-{year}" .format(
                day = str(random.randint(1,28)),
                month = str(random.randint(1,12)),
                year = random.choice([str(random.randint(0, 1700)),
                                      str(random.randint(2030, 2200))]))

        elif self.incorrect_elem == 4:
            self.exp_date = "{day}-{month}-{year}".format(
            day = str(random.randint(1,28)),
            month = str(random.randint(1,12)),
            year = str (random.randint(0, 2020)))

        elif self.incorrect_elem == 5:
            self.iss_city = random.choice(["Mordor","Camelot",
                                           "Caladan","Giedi Prime",
                                           "Hell","Demacia"])
