import math
from dataclasses import dataclass, field
from typing import Literal

from icecream import ic

DISTANCE_DOOR = .2
DISTANCE_KEY = .2
DISTANCE_DANGER = .2

# TODO: Game state is buggy with multiple puzzle objects, for now we can add a function directly into the
# puzzle data class to evaluate distance and proximity to agent class. this way we can make sure that each object
# call on this function to interact with game states.


@dataclass
class CollisionState:
    left: bool = field(default=False)
    right: bool = field(default=False)
    up: bool = field(default=False)
    down: bool = field(default=False)
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
