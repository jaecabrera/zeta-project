import json
from typing import Literal, Union, Optional

import pyglet.image
import numpy as np

from agent import Agent
from util.common_imports import *


@dataclass(repr=True)
class PuzzleData:
    """Class for representing puzzle data."""
    puzzle_type: Literal['key', 'door', 'trap', 'wall', 'flag']
    ref_color: Literal['blue', 'red', 'None']
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
                 puzzle_data: PuzzleData | pyglet.image.Animation):
        self.data = puzzle_data

        super().__init__(self.data.image, x, y, batch=self.data.batch)

    def transparent_collider(self, agent: Agent):
        # TODO: puzzle object proximity to agent

        distance = 50

        # Calculate boundaries
        left = self.x - distance
        right = self.x + self.width + distance
        bottom = self.y - distance
        top = self.y + self.height + distance

        # Check if agent is in proximity
        if left <= agent.x <= right and bottom <= agent.y <= top:
            return True

        return False


PUZZLE_DATA = {
    'b': PuzzleData(puzzle_type='box', ref_color='None'),
    'rd': PuzzleData(puzzle_type='door', ref_color='red'),
    'bd': PuzzleData(puzzle_type='door', ref_color='blue'),
    'sp': PuzzleData(puzzle_type='trap', ref_color='None'),
    'rs': PuzzleData(puzzle_type='key', ref_color='red'),
    'bs': PuzzleData(puzzle_type='key', ref_color='blue'),
    'fl': PuzzleData(puzzle_type='flag', ref_color='blue')
}
