import math
import arcade
import random
import assets

from enum import Enum
from person import Person
from item import Item
from id_card import IdCard

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Lost Item Please"

IMAGE_SIZE = 500

GRID_ITEM_SIZE = IMAGE_SIZE * Item.SCALE * .8
GRID_ITEM_RAND_MAX_OFFSET = 40
GRID_POS = (SCREEN_WIDTH - 4 * GRID_ITEM_SIZE, GRID_ITEM_SIZE)

ITEM_PLACE_RANGE = (IMAGE_SIZE + GRID_ITEM_SIZE) / 2 / 1.7

def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

def is_playing(player):
    return player is not None and player.playing

class State(Enum):
    # Game states
    CHOOSING        = 0
    ITEM_PLACED     = 1

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
        self.init_items()
        self.init_person()
        self.state = State.CHOOSING
        self.sound_player = None

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        self.person.draw()
        for item in self.items: item.draw()

    def on_update(self, delta):
        """ Game logic """
        self.person.update(delta)
        for item in self.items: item.update(delta)
        if self.held_item is not None:
            self.held_item.move(self.mouse_x, self.mouse_y)


        if self.state == State.ITEM_PLACED and not self.person.is_traveling:
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
            self.init_person()


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


    def init_idcard(self):
        self.idcard = IdCard(self.person, "2020-01-21", random.choices([True, False],[70,30]))


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
                   self.state = State.ITEM_PLACED
                   self.items.remove(self.held_item)
                   self.person.give_item(self.held_item)

            self.held_item.x = self.held_item.orig_x
            self.held_item.y = self.held_item.orig_y
            self.held_item = None

    def on_mouse_motion(self, x, y, _dx, _dy):
        """ Handle mouse release """
        self.mouse_x = x
        self.mouse_y = y


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
