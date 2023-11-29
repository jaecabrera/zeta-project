from common_imports import *


class WallGenerator:

    def __init__(self, image, win_height, win_width, batch):
        self.image = image
        self.default_x = 0
        self.default_y = 0
        self.box_width = 32
        self.box_sprites = list()
        self.create_boundary_box(win_height, win_width, batch)

    def generate_box(self, x, y, batch) -> None:
        """
        Generates a 32x32 Sprite Box Object in the field which will be added
        to the `box_batch` sprite batch.
        :param x: x-coordinate spawn position
        :param y: y-coordinate spawn position
        :return: None
        """

        self.box_sprites.append(pyg.sprite.Sprite(self.image, x, y, batch=batch))

    def create_boundary_box(self, window_height, window_width, batch):

        """ Boundary Box """
        for i in np.arange(1024, step=self.box_width):
            self.generate_box(i, 0, batch)

        for i in np.arange(768, step=self.box_width):
            self.generate_box(0, i, batch)

        for i in np.arange(1024, step=self.box_width):
            self.generate_box(i, window_height - 32, batch)

        for i in np.arange(1024, step=self.box_width):
            self.generate_box(window_width - 32, i, batch)
