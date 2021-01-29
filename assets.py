import os
import arcade

image_names = os.listdir("res/image")
person_names = [name[:-4] for name in image_names]
print(person_names, flush=True)

images = list(map(lambda n: arcade.load_texture("res/image/" + n), image_names))

persons = { name: image for name, image in zip(person_names, images) }
