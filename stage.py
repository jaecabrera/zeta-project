from typing import Literal

import pyglet.window

from util.common_imports import *


class WallGenerator:

    def __init__(self, image, win_height, win_width, batch):
        self.image = image
        self.default_x = 0
        self.default_y = 0
        self.box_width = 32
        self.box_sprites = list()
        self.create_boundary_box(win_height, win_width, batch)

    def generate_box(self, x, y, batch: pyglet.graphics.Batch) -> None:
        """
        Generates a 32x32 Sprite Box Object in the field which will be added
        to the `box_batch` sprite batch.
        :param batch: Pyglet Batch Object for drawing all wall in batch instead of individual sprite obj.
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


def set_stage(wall: WallGenerator, window: pyglet.window.Window, box_batch: pyglet.graphics.Batch,
              structure: Literal['stage_1']) -> None:
    """
    Sets the current stage for the game where stage is defined as the puzzle structure.
    :param structure: Sets the structure stage level among the ff. ['stage-1', ...]
    :param wall: Wall Object to be used for the stage
    :param window: Pyglet Window  Object to be used as reference
    :param box_batch: Pyglet Batch Object for drawing all wall in batch instead of individual sprite obj.
    :return:
    """
    if structure == 'stage_1':

        # columns
        for i in np.arange(32, 768 // 2, step=32):
            wall.generate_box(window.width // 2, y=i, batch=box_batch)

        for i in np.arange(768 // 2 + 32, 768, step=32):
            wall.generate_box(window.width // 2, y=i, batch=box_batch)

        for i in np.arange(window.width // 4, step=32):
            wall.generate_box(x=i, y=window.height // 4, batch=box_batch)

        for i in np.arange(window.width // 4, step=32):
            wall.generate_box(x=i, y=window.height // 4, batch=box_batch)

        for i in np.arange(window.height // 4, window.height // 2, step=32):
            wall.generate_box(x=window.width // 4, y=i, batch=box_batch)

        for i in np.arange(64, 32 * 6, step=32):
            wall.generate_box(x=window.width // 4, y=i, batch=box_batch)

        # rows

        for i in np.arange(32 * 14, 768, step=32):
            wall.generate_box(x=window.width // 4, y=i, batch=box_batch)

        for i in np.arange(32, window.width // 4 - 32, step=32):
            wall.generate_box(x=i, y=32 * 11, batch=box_batch)

        for i in np.arange(32, window.width // 4 - 32, step=32):
            wall.generate_box(x=i, y=32 * 18, batch=box_batch)

        for i in np.arange(32 * 9, 32 * 12, step=32):
            wall.generate_box(x=i, y=32 * 7, batch=box_batch)

        for i in np.arange(32 * 13, 32 * 17, step=32):
            wall.generate_box(x=i, y=32 * 7, batch=box_batch)

        for i in np.arange(32 * 9, 32 * 12, step=32):
            wall.generate_box(x=i, y=32 * 7, batch=box_batch)

        for i in np.arange(32 * 10, 32 * 17, step=32):
            wall.generate_box(x=i, y=32 * 11, batch=box_batch)

        for i in np.arange(32 * 9, 32 * 17, step=32):
            wall.generate_box(x=i, y=32 * 14, batch=box_batch)