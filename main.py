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
from strikes import Strikes


# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Lost Item Please"

IMAGE_SIZE = 500

GRID_ITEM_SIZE = IMAGE_SIZE * Item.SCALE * .8
GRID_ITEM_RAND_MAX_OFFSET = 40
GRID_POS = (SCREEN_WIDTH - 4 * GRID_ITEM_SIZE, GRID_ITEM_SIZE)

ITEM_PLACE_RANGE = (IMAGE_SIZE + GRID_ITEM_SIZE) / 2 / 1.7

BUTTON_POS = (915, 195)

CLOCK_POS = (910, 400)

STRIKES_POS = (915, 68)

NOTE_POS = (400, 300)

def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

def is_playing(player):
    return player is not None and player.playing

class State(Enum):
    # Game states
    DAY_INTRO       = 0
    DAY_FADE_IN     = 1
    DAY_FADE_OUT    = 2
    CHOOSING        = 3
    CHOICE_MADE     = 4
    END_FADE_OUT    = 5
    END_SCREEN      = 6
    START_SCREEN    = 7
    START_FADE_OUT  = 8
    START_FADE_IN   = 9

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

    def setup(self, restart=False):
        """ Set up the game here. Call this function to restart the game. """
        self.note = Note(*NOTE_POS)
        self.button = Button(*BUTTON_POS)
        self.clock = Clock(*CLOCK_POS)
        self.strikes = Strikes(*STRIKES_POS)
        self.init_items()
        self.init_person()
        self.init_idcard()
        self.state = State.START_FADE_IN
        self.state_time = 0
        self.day = 1
        self.score = 0
        self.guide_visible = False

        if not restart:
            self.sound_player = None
            arcade.play_sound(assets.sounds['elevator_music'], volume=0.03, looping=True)
            self.set_fullscreen(True)

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()

        if self.state in [State.START_SCREEN, State.START_FADE_OUT, State.START_FADE_IN]:
            arcade.draw_scaled_texture_rectangle(SCREEN_WIDTH / 2,
                                                 SCREEN_HEIGHT / 2,
                                                 assets.intro_image,
                                                 1,
                                                 0)
            if self.guide_visible:
                arcade.draw_scaled_texture_rectangle(SCREEN_WIDTH / 2,
                                                     SCREEN_HEIGHT / 2,
                                                     assets.guide_image,
                                                     1,
                                                     0)
                arcade.draw_scaled_texture_rectangle(SCREEN_WIDTH - 200,
                                                     100,
                                                     assets.close_image,
                                                     .5,
                                                     0)
            if self.state == State.START_FADE_OUT:
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    (0, 0, 0, max(int(self.state_time * 255), 0))
                )
            elif self.state == State.START_FADE_IN:
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH / 2,
                    SCREEN_HEIGHT / 2,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    (0, 0, 0, max(int((1 - self.state_time) * 255), 0))
                )
            return

        arcade.draw_scaled_texture_rectangle(SCREEN_WIDTH / 2,
                                             SCREEN_HEIGHT / 2,
                                             assets.bg_image,
                                             1,
                                             0)
        self.button.draw()


        self.person.draw()
        self.id_card.draw()

        self.clock.draw()
        self.note.draw()
        self.strikes.draw()
        for item in reversed(self.items): item.draw()

        if self.state == State.DAY_FADE_IN:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, max(int((1 - self.state_time) * 255), 0))
            )
        elif self.state in [State.DAY_FADE_OUT, State.END_FADE_OUT]:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                (0, 0, 0, max(int(self.state_time * 255), 0))
            )
        elif self.state == State.DAY_INTRO:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                arcade.color.BLACK
            )
            if self.state_time < 4:
                color = (min(int(self.state_time * 255), 255),) * 3
            else:
                color = (min(int((5 - self.state_time) * 255), 255),) * 3
            arcade.draw_text(
                f"Day {['one', 'two', 'three'][self.day-1]}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                color,
                48,
                align="center",
                anchor_x="center",
                anchor_y="center"
            )
        elif self.state == State.END_SCREEN:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                arcade.color.BLACK
            )
            text = f"You correctly returned {self.score} lost items."
            if self.strikes.strikes == 3:
                text = f"You have been fired for returning items wrongly.\n\n{text}"
            text = f"{text}\n\n\n\nPress R to play again."
            color = (min(int(self.state_time * 255), 255),) * 3
            arcade.draw_text(
                text,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                color,
                48,
                align="center",
                anchor_x="center",
                anchor_y="center"
            )


    def on_update(self, delta):
        """ Game logic """
        self.state_time += delta

        if self.state in [State.END_SCREEN, State.START_SCREEN]:
            return
        elif self.state == State.DAY_FADE_IN:
            if self.state_time > 1:
                self.transition(State.CHOOSING)
            return
        elif self.state == State.START_FADE_IN:
            if self.state_time > 1:
                self.transition(State.START_SCREEN)
            return
        elif self.state == State.START_FADE_OUT:
            if self.state_time > 1:
                self.transition(State.DAY_INTRO)
        elif self.state == State.END_FADE_OUT:
            if self.state_time > 1:
                self.transition(State.END_SCREEN)
        elif self.state == State.DAY_FADE_OUT:
            if self.state_time > 1:
                self.transition(State.DAY_INTRO)
                self.advance_day()
            return
        elif self.state == State.DAY_INTRO:
            if self.state_time > 5:
                self.transition(State.DAY_FADE_IN)
            return

        self.person.update(delta)
        self.clock.update(delta)
        for item in self.items: item.update(delta)
        if self.held_item is not None:
            self.held_item.move(self.mouse_x, self.mouse_y)


        if self.state == State.CHOICE_MADE and not self.person.is_traveling:
            self.transition(State.CHOOSING)

        if self.state == State.CHOOSING and self.strikes.strikes == 3:
            self.transition(State.END_FADE_OUT)


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

            if self.clock.is_completed():
                self.transition(State.DAY_FADE_OUT)
                self.person.state = State.WAITING
                return

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
        self.person = Person(0, SCREEN_HEIGHT + IMAGE_SIZE)
        self.person.travel_to(500, 800, spin=False)
        self.person.set_state(State.ENTER)
        self.person.pick_item(self.items)
        self.note.set_item(self.person.wanted_item.name)
        self.note.set_person_name(self.person.name)
        self.note.randomize_fake()


    def init_idcard(self):
        """
        Inits the id card of the current person with a 30% chance of the
        card being false.
        """
        self.id_card = IdCard(self.person, True if random.randint(0,100) < 30 else False)

    def transition(self, state):
        """ Changes state """
        self.state = state
        self.state_time = 0

    def advance_day(self):
        """ Move to the next day """
        if self.day == 3:
            self.transition(State.END_SCREEN)
        self.day = (self.day % 3) + 1
        self.note.day = self.day
        self.clock.time = 0
        self.init_items()
        self.init_person()
        self.init_idcard()

    def get_strike(self):
        arcade.play_sound(assets.sounds['strike'])
        self.strikes.strikes += 1
        if self.strikes.strikes == 3:
            self.transition(State.END_FADE_OUT)

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

        if dist(self.button.x, self.button.y, x, y) < 70 * Button.SCALE:
            if self.state == State.CHOOSING:
               new_x = self.person.x - 1.5 * IMAGE_SIZE
               self.person.set_state(State.AWAY_WRONG)
               self.person.travel_to(new_x, SCREEN_HEIGHT + IMAGE_SIZE)
               self.transition(State.CHOICE_MADE)
               if not self.note.is_fake and not self.id_card.is_false():
                   self.get_strike()

        if self.state == State.START_SCREEN:
            if self.guide_visible:
                self.guide_visible = False
                arcade.play_sound(assets.sounds['click'])
            elif 350 < y and y < 600:
                if 1030 < x and x < 1500:
                    self.guide_visible = True
                    arcade.play_sound(assets.sounds['click'])
                if 470 < x and x < 940:
                    self.transition(State.START_FADE_OUT)
                    arcade.play_sound(assets.sounds['click'])


    def on_mouse_release(self, x, y, button, _modifiers):
        """ Handle mouse release """
        if button != 1: # Left
            return

        if self.held_item is not None:
            if self.state == State.CHOOSING \
               and dist(x, y, self.person.x, self.person.y) < ITEM_PLACE_RANGE:
                self.transition(State.CHOICE_MADE)
                if self.person.wanted_item.name == self.held_item.name:
                    new_x = self.person.x + 1.5 * IMAGE_SIZE
                    self.person.set_state(State.AWAY_RIGHT)
                    if self.note.is_fake or self.id_card.is_false():
                        self.get_strike()
                    else:
                        self.score += 1
                else:
                    new_x = self.person.x - 1.5 * IMAGE_SIZE
                    self.person.set_state(State.AWAY_WRONG)
                    self.get_strike()

                self.person.travel_to(new_x, SCREEN_HEIGHT + IMAGE_SIZE)
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
        elif key in [arcade.key.ESCAPE, arcade.key.Q]:
            exit()
        elif key == arcade.key.R:
            if self.state == State.END_SCREEN:
                self.setup(restart=True)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
