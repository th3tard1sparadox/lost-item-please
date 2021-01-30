import math
import arcade
import random
import assets

from enum import Enum
from person import Person
from item import Item
from id_card import IdCard

from button import Button
from clock import Clock
from note import Note




# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Lost Item Please"

IMAGE_SIZE = 500

GRID_ITEM_SIZE = IMAGE_SIZE * Item.SCALE * .8
GRID_ITEM_RAND_MAX_OFFSET = 40
GRID_POS = (SCREEN_WIDTH - 4 * GRID_ITEM_SIZE, GRID_ITEM_SIZE)

ITEM_PLACE_RANGE = (IMAGE_SIZE + GRID_ITEM_SIZE) / 2 / 1.7

BUTTON_POS = (950, 200)

CLOCK_POS = (950, 400)

NOTE_POS = (400, 300)

def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

def is_playing(player):
    return player is not None and player.playing

class State(Enum):
    # Game states
    CHOOSING        = 0
    CHOICE_MADE     = 1

    # Person states
    ENTER           = 10
    INTRO           = 11
    DESCRIBE        = 12
    WAITING         = 13
    AWAY_RIGHT      = 14
    AWAY_WRONG      = 15
    EXIT            = 16

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.note = Note(*NOTE_POS)
        self.button = Button(*BUTTON_POS)
        self.clock = Clock(*CLOCK_POS)
        self.init_items()
        self.init_person()
        self.init_idcard()
        self.state = State.CHOOSING
        self.sound_player = None

        self.set_fullscreen(True)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        self.person.draw()
        self.id_card.draw()

        self.button.draw()
        self.clock.draw()
        self.note.draw()
        for item in reversed(self.items): item.draw()





    def on_update(self, delta):
        """ Game logic """
        self.person.update(delta)
        self.clock.update(delta)
        for item in self.items: item.update(delta)
        if self.held_item is not None:
            self.held_item.move(self.mouse_x, self.mouse_y)


        if self.state == State.CHOICE_MADE and not self.person.is_traveling:
            self.state = State.CHOOSING


        if self.person.state == State.ENTER and not self.person.is_traveling:
            self.person.set_state(State.INTRO)

        elif self.person.state == State.INTRO:
            if not is_playing(self.sound_player):
                self.sound_player = self.person.play_sound("intro")
                self.person.set_state(State.DESCRIBE)

        elif self.person.state == State.DESCRIBE:
            if not is_playing(self.sound_player):
                self.sound_player = self.person.wanted_item.play_sound()
                self.person.set_state(State.WAITING)

        elif self.person.state in [State.AWAY_RIGHT, State.AWAY_WRONG]:
            if not is_playing(self.sound_player):
                if self.person.state == State.AWAY_RIGHT:
                    sound = "right"
                else:
                    sound = "wrong"
                self.sound_player = self.person.play_sound(sound)
                self.person.set_state(State.EXIT)

        elif self.person.state == State.EXIT and not self.person.is_traveling:

            if self.id_card.is_false():
                print(self.id_card.invalidity_reason())

            self.init_person()
            self.init_idcard()

    def init_items(self):
        """ Create a 3x4 grid of items """
        self.held_item = None
        self.items = []
        available_items = random.sample(list(assets.items), 12)

        for r in range(3):
            for c in range(4):
                ox, oy = GRID_POS
                rangle = math.pi * 2 * random.random()
                rlength = GRID_ITEM_RAND_MAX_OFFSET * random.random()**.3
                rx, ry = math.cos(rangle) * rlength, math.sin(rangle) * rlength
                self.items.append(
                    Item(ox + rx + GRID_ITEM_SIZE * c,
                         oy + ry + GRID_ITEM_SIZE * r,
                         available_items.pop())
                )

    def init_person(self):
        """ Create a person that travels to its position """
        self.person = Person(100, 100)
        self.person.travel_to(500, 800)
        self.person.set_state(State.ENTER)
        self.person.pick_item(self.items)
        self.note.set_text(assets.descriptions[self.person.wanted_item.name])


    def init_idcard(self):
        """
        Inits the id card of the current person with a 30% chance of the
        card being false.
        """
        self.id_card = IdCard(self.person, random.choices([True, False],[30,70]))


    def on_mouse_press(self, x, y, button, _modifiers):
        """ Handle mouse press """
        if button != 1: # Left
            return

        if self.held_item is not None:
            return

        for item in self.items:
            if dist(item.x, item.y, x, y) < IMAGE_SIZE / 2 * Item.SCALE * .9:
                self.held_item = item
                break

        if dist(self.button.x, self.button.y, x, y) < IMAGE_SIZE / 2 * Button.SCALE * .9:
            if self.state == State.CHOOSING:
               new_x = self.person.x - IMAGE_SIZE
               self.person.set_state(State.AWAY_WRONG)
               self.person.travel_to(new_x, SCREEN_HEIGHT + IMAGE_SIZE)
               self.state = State.CHOICE_MADE


    def on_mouse_release(self, x, y, button, _modifiers):
        """ Handle mouse release """
        if button != 1: # Left
            return

        if self.held_item is not None:
            if self.state == State.CHOOSING \
               and dist(x, y, self.person.x, self.person.y) < ITEM_PLACE_RANGE:
                   if self.person.wanted_item.name == self.held_item.name:
                       new_x = self.person.x + IMAGE_SIZE
                       self.person.set_state(State.AWAY_RIGHT)
                   else:
                       new_x = self.person.x - IMAGE_SIZE
                       self.person.set_state(State.AWAY_WRONG)

                   self.person.travel_to(new_x, SCREEN_HEIGHT + IMAGE_SIZE)
                   self.state = State.CHOICE_MADE
                   self.items.remove(self.held_item)
                   self.person.give_item(self.held_item)

            self.held_item.x = self.held_item.orig_x
            self.held_item.y = self.held_item.orig_y
            self.held_item = None

    def on_mouse_motion(self, x, y, _dx, _dy):
        """ Handle mouse release """
        self.mouse_x = x
        self.mouse_y = y

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        if key in [arcade.key.ESCAPE, arcade.key.Q]:
            exit()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
