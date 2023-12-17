from dataclasses import dataclass
import logging
from agent import Agent
from game import GoblinAI
from loader import GAME_SPECS, AGENT_PARAMS, STAGE_A, IMAGE_MANAGER
from util.puzzle import PUZZLE_DATA
import pyglet as pyg
import time


# TODO: Remove this class
@dataclass
class TrainVariables:
    state_old = ...
    move = ...
    reward = ...
    done = ...
    score = ...


class TrainerGoblinAI:

    def __init__(self):
        self.g = GoblinAI(
            **GAME_SPECS.get_window_params(),
            f_screen=False,
            _agent=Agent(**AGENT_PARAMS),
            img_manager=IMAGE_MANAGER,
            puzzle_data=PUZZLE_DATA,
            stage=STAGE_A,
            trainer_variable=TrainVariables())

        pyg.clock.schedule_interval(self.g.update, 1 / 60.0)
        self.app = pyg.app
        self.app.run()

    def update_trainer_variables(self, state_old, move, reward, state_new, done):
        ...

    def train_agent(self):
        self.g.tv.state_old = self.g.state.get_state()
        self.g.tv.move = self.g.agent.get_action(self.tv.state_old)

        # self.g._move(self.move)

        self.g.tv.reward, self.g.tv.done, self.g.tv.score = self.g.get_game_data()
        self.g.tv.state_new = self.g.state.get_state()

        # return state_old, final_move, reward, state_new, done

    def close_game(self):
        for i in range(5, 0, -1):
            print(f'closing the game in ..{i} second/s')
            time.sleep(1)

        self.app.exit()


if __name__ == '__main__':
    g = TrainerGoblinAI()
    # g.close_game()
