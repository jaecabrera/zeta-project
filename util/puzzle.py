import json
from typing import Literal, Union, Optional

import pyglet
import pyglet.image

from util.common_imports import *


@dataclass(repr=True)
class PuzzleData:
    """Class for representing puzzle data."""
    puzzle_type: Literal['key', 'door', 'trap', 'wall']
    ref_color: Literal['blue', 'red', 'None', 'None']
    _image: pyglet.image.AbstractImage = None
    _batch: Optional[pyglet.graphics.Batch] = None

    @property
    def batch(self):
        return self._batch

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image_manager_image_obj):
        self._image = image_manager_image_obj

    def create_batch(self):
        """Create and initialize a batch for the puzzle data."""
        self._batch = pyg.graphics.Batch()
        return self


class PuzzleObject(pyg.sprite.Sprite):

    def __init__(self,
                 x: Union[int, float],
                 y: Union[int, float],
                 puzzle_data: PuzzleData):
        self.data = puzzle_data

        super().__init__(self.data.image, x, y, batch=self.data.batch)


PUZZLE_DATA = {
    'b': PuzzleData(puzzle_type='box', ref_color='None'),
    'rd': PuzzleData(puzzle_type='door', ref_color='red'),
    'bd': PuzzleData(puzzle_type='door', ref_color='blue'),
    'sp': PuzzleData(puzzle_type='trap', ref_color='None'),
    'rs': PuzzleData(puzzle_type='key', ref_color='red'),
    'bs': PuzzleData(puzzle_type='key', ref_color='blue')
}
