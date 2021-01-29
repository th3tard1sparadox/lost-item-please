import arcade
from person import Person
from item import Item

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Lost Item Please"

IMAGE_SIZE = 500

def dist(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

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
        """ Game logic """
        self.person.update(delta)
        for item in self.items: item.update(delta)
        if self.held_item is not None:
            self.held_item.move(self.mouse_x, self.mouse_y)

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

    def on_mouse_release(self, _x, _y, button, _modifiers):
        """ Handle mouse release """
        if button != 1: # Left
            return

        if self.held_item is not None:
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
