from typing import Literal, Union, Optional

import pyglet.image

from common_imports import *


@dataclass(repr=True)
class PuzzleData:
    """Class for representing puzzle data."""
    puzzle_type: Literal['key', 'door', 'trap']
    ref_color: Literal['blue', 'red', 'None']
    image: pyglet.image.AbstractImage
    _batch: Optional[pyglet.graphics.Batch] = None

    @property
    def batch(self):
        return self._batch

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
