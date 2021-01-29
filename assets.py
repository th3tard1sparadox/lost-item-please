import os
import arcade

PERSON_DIR = "res/image/person"
ITEM_DIR = "res/image/item"

def load_dir(path):
    """
    Load all assets in given path.
    """
    image_names = os.listdir(path)
    names = [name[:name.index(".")] for name in image_names]
    images = list(map(lambda n: arcade.load_texture(f"{path}/{n}"), image_names))

    return names, images

persons = { name: image for name, image in zip(*load_dir(PERSON_DIR)) }
items = { name: image for name, image in zip(*load_dir(ITEM_DIR)) }
