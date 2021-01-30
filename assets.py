import os
import arcade

PERSON_DIR = "res/image/person"
ITEM_DIR = "res/image/item"
SOUND_DIR = "res/sound"

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
