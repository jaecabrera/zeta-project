from common_imports import *

""" Wall Sprite """
wall_filepath = Path.cwd() / "assets" / "sprite" / "wall" / "crate.png"
wall_image = pyg.image.load(wall_filepath)


class Box(pyg.sprite.Sprite):

    def __init__(self, x, y, batch=None):
        super().__init__(pyg.sprite.Sprite(wall_image), x, y)
