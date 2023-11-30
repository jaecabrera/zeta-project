import pyglet.window
from typing import Literal

from common_imports import *
from puzzle import PuzzleData, PuzzleObject
from settings import PIXEL


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

        for i in np.arange(32 * 14, 768, step=32):
            wall.generate_box(x=window.width // 4, y=i, batch=box_batch)

        for i in np.arange(32, window.width // 4 - 32, step=32):
            wall.generate_box(x=i, y=32 * 11, batch=box_batch)

        for i in np.arange(32, window.width // 4 - 32, step=32):
            wall.generate_box(x=i, y=32 * 18, batch=box_batch)


def set_objects() -> dict:
    return {'door': create_doors(),
            'shroom': create_shroom(),
            'trap': create_traps()}


def create_doors():
    door_blue_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door_blue.png"

    blue_door_image = pyg.image.load(door_blue_filepath)
    blue_door_pos: list[tuple] = [(32 * 16, 32 * 12)]
    blue_door_data = PuzzleData(puzzle_type="door", ref_color="blue", image=blue_door_image)
    blue_door_data.create_batch()
    blue_door_list = [PuzzleObject(x, y, blue_door_data) for x, y in blue_door_pos]

    # create red doors - puzzle data
    red_door_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door.png"
    red_door_image = pyg.image.load(red_door_filepath)
    red_door_pos: list[tuple] = [
        (32 * 7, 32 * 11),
        (32 * 7, 32 * 18)
    ]
    red_door_data = PuzzleData(puzzle_type="door", ref_color="red", image=red_door_image)
    red_door_data.create_batch()
    red_door_list = [PuzzleObject(x, y, red_door_data) for x, y in red_door_pos]

    return [blue_door_list, blue_door_data], [red_door_list, red_door_data]


def create_shroom():
    # Mushrooms

    red_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "red_mush.png"
    red_shroom_image = pyg.image.load(red_shroom_fp)
    red_shroom_pos: list[tuple] = [(82, 472), (82, 280)]
    red_shroom_data = PuzzleData(puzzle_type="key", ref_color="red", image=red_shroom_image)
    red_shroom_data.create_batch()
    red_shroom_list = [PuzzleObject(x, y, red_shroom_data) for x, y in red_shroom_pos]

    blue_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "blue_mush.png"
    blue_shroom_image = pyg.image.load(blue_shroom_fp)
    blue_shroom_pos: list[tuple] = [(76, 668)]
    blue_shroom_data = PuzzleData(puzzle_type="key", ref_color="blue", image=blue_shroom_image)
    blue_shroom_data.create_batch()
    blue_shroom_list = [PuzzleObject(x, y, blue_shroom_data) for x, y in blue_shroom_pos]

    return [red_shroom_list, red_shroom_data], [blue_shroom_list, blue_shroom_data]


def create_traps():
    # trap
    trap_sprite_fp = Path.cwd() / "assets" / "sprite" / "trap" / "spike.png"
    trap_image = pyg.image.load(trap_sprite_fp)
    trap_pos: list[tuple] = [(PIXEL * i, 190) for i in np.arange(9, 12, step=1)]
    [trap_pos.append((PIXEL * x, 190)) for x in np.arange(13, 16, step=1)]

    trap_data = PuzzleData(puzzle_type="trap", ref_color="None", image=trap_image)
    trap_data.create_batch()
    trap_list = [PuzzleObject(x, y, trap_data) for x, y in trap_pos]

    return trap_data, trap_list
