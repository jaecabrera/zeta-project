from dataclasses import dataclass
import logging
from agent import Agent
from game import GoblinAI
from loader import GAME_SPECS, AGENT_PARAMS, STAGE_A, IMAGE_MANAGER
from util.puzzle import PUZZLE_DATA
import pyglet as pyg
import time
from IPython import display


class TrainerGoblinAI:

    def __init__(self):
        self.g = GoblinAI(
            **GAME_SPECS.get_window_params(),
            f_screen=False,
            _agent=Agent(**AGENT_PARAMS),
            img_manager=IMAGE_MANAGER,
            puzzle_data=PUZZLE_DATA,
            stage=STAGE_A)

        pyg.clock.schedule_interval(self.g.update, 1 / 60.0)
        self.app = pyg.app
        self.app.run()


if __name__ == '__main__':
    g = TrainerGoblinAI()
