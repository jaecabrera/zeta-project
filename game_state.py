import math
from dataclasses import dataclass, field
from typing import Literal

from icecream import ic


@dataclass
class CollisionState:
    left: bool = field(default=False)
    right: bool = field(default=False)
    up: bool = field(default=False)
    down: bool = field(default=False)
    nearby_door: bool = field(default=False)
    nearby_key: bool = field(default=False)
    nearby_danger: bool = field(default=False)
    distance: float = field(default=float)

    puzzle_distance_constant = 400

    @staticmethod
    def check_distance(agent, puzzle_obj):
        return math.sqrt(((agent.x - puzzle_obj.x) ** 2) + ((agent.y - puzzle_obj.y) ** 2))

    def update_state(self, agent, puzzle_obj,
                     _state: Literal['direction', 'nearby_key', 'nearby_danger', 'nearby_door']) \
            -> None:

        match _state:

            case 'nearby_key':
                self.nearby_key = self.check_distance(agent, puzzle_obj) <= 100

            case 'nearby_door':
                self.nearby_door = self.check_distance(agent, puzzle_obj) <= 50

            case 'nearby_danger':
                self.nearby_danger = self.check_distance(agent, puzzle_obj) <= 100
