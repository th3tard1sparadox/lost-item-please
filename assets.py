import os
import arcade

PERSON_DIR = "res/image/person"
ITEM_DIR = "res/image/item"
BACKGROUND_DIR = "res/image/background"
SOUND_DIR = "res/sound"
DESC_DIR = "res/desc/"

def load_dir(path, loader):
    """
    Load all assets in given path.
    """
    asset_names = os.listdir(path)
    names = [name[:name.index(".")] for name in asset_names]
    assets = list(map(lambda n: loader(f"{path}/{n}"), asset_names))

    return { name: image for name, image in zip(names, assets) }

persons = load_dir(PERSON_DIR, arcade.load_texture)
items = load_dir(ITEM_DIR, arcade.load_texture)
sounds = load_dir(SOUND_DIR, arcade.load_sound)
backgrounds = load_dir(BACKGROUND_DIR, arcade.load_texture)
descriptions = {}

with open(DESC_DIR + "items.txt", 'r') as file:
    lines = file.readlines()

for line in lines:
    split_line = line.split(': ')
    descriptions[split_line[0]] = split_line[1]

clock_image = arcade.load_texture("res/image/clock.png")
note_image = arcade.load_texture("res/image/note.png")
picture_image = arcade.load_texture("res/image/picture.png")
bg_image = arcade.load_texture("res/image/bg.png")
button_image = arcade.load_texture("res/image/button.png")
kallellse_image = arcade.load_texture("res/image/kallellse.png")
kallellse_wrong_image = arcade.load_texture("res/image/kallellse_wrong.png")
strike_image = arcade.load_texture("res/image/strike.png")
not_strike_image = arcade.load_texture("res/image/not_strike.png")
