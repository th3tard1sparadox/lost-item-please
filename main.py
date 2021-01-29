import arcade
from person import Person
from item import Item

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Lost Item Please"

IMAGE_SIZE = 500

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
        self.person = Person(100, 100)
        self.person.travel_to(500, 800)

        self.held_item = None
        self.items = [Item(1500, 200)]

    def on_draw(self):
        """ Render the screen. """

        arcade.start_render()
        self.person.draw()

        for item in self.items: item.draw()

    def on_update(self, delta):
        """ Game logics """
        self.person.update(delta)
        for item in self.items: item.update(delta)

    def on_mouse_press(self, x, y, button, _modifiers):
        """ Handle mouse press """
        if button != 1: # Left
            return

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
