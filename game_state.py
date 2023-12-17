import math
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

DISTANCE_DOOR = .4
DISTANCE_KEY = .4
DISTANCE_DANGER = .4

# TODO: Add core states here
@dataclass
class CollisionState:
    # left: bool = field(default=False)
    # right: bool = field(default=False)
    # up: bool = field(default=False)
    # down: bool = field(default=False)
    colliding_with_trap: bool = field(default=False)
    colliding_with_door: bool = field(default=False)
    holding_key: bool = field(default=False)
    colliding_with_wall: bool = field(default=False)
    nearby_red_door: bool = field(default=False)
    nearby_blue_door: bool = field(default=False)
    nearby_red_key: bool = field(default=False)
    nearby_blue_key: bool = field(default=False)
    nearby_danger: bool = field(default=False)

    @staticmethod
    def check_distance(agent, puzzle_obj, algorithm: Literal['euc', 'manh', 'perc']):
        match algorithm:
            case 'euc':
                return math.sqrt(((agent.x - puzzle_obj.x) ** 2) + ((agent.y - puzzle_obj.y) ** 2))
            case 'manh':
                return abs(agent.x - puzzle_obj.x) + abs(agent.y - puzzle_obj.y)
            case 'perc':
                return agent.x - puzzle_obj.x / puzzle_obj.x * 100

    def get_state(self):
        # TODO: add get states here
        return np.array([self.colliding_with_trap, self.colliding_with_door, self.holding_key, self.colliding_with_wall, self.nearby_red_door, self.nearby_blue_door,
                         self.nearby_red_key, self.nearby_blue_key, self.nearby_danger],
                        dtype='int')

    def update_state(self, agent, puzzle_obj,
                     _state: Literal[
                         'direction', 'nearby_red_key', 'nearby_blue_key', 'nearby_danger', 'nearby_red_door',
                         'nearby_blue_door']) \
            -> None:
        global DISTANCE_DOOR
        global DISTANCE_KEY
        global DISTANCE_DANGER
        match _state:

            case 'nearby_red_key':
                self.nearby_red_key = self.check_distance(agent, puzzle_obj, algorithm='euc') <= DISTANCE_KEY

            case 'nearby_blue_key':
                self.nearby_blue_key = self.check_distance(agent, puzzle_obj, algorithm='euc') <= DISTANCE_KEY

            case 'nearby_blue_door':
                self.nearby_blue_door = self.check_distance(agent, puzzle_obj, algorithm='euc') <= DISTANCE_DOOR

            case 'nearby_red_door':
                self.nearby_red_door = self.check_distance(agent, puzzle_obj, algorithm='euc') <= DISTANCE_DOOR

            case 'nearby_danger':
                self.nearby_danger = self.check_distance(agent, puzzle_obj, algorithm='euc') <= DISTANCE_DANGER
