from collections import deque
from random import sample

import matplotlib.pyplot as plt
import torch
from IPython import display
from icecream import ic
from pyglet.window.key import KeyStateHandler

import game
from inventory_system import Inventory
from loader import GAME_SPECS, AGENT_PARAMS, IMAGE_MANAGER, STAGE_A
from model import Linear_QNet, QTrainer
from util.common_imports import *
from util.puzzle import PUZZLE_DATA

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


@dataclass
class MovementManager:
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False

    def move(self, direction: str, state: bool):
        match direction:
            case 'left':
                self.left = state
            case 'up':
                self.up = state
            case 'down':
                self.down = state
            case 'right':
                self.right = state


class Agent(pyg.sprite.Sprite, MovementManager):

    def __init__(self, sprite_grid, x, y, spd):
        super(Agent, self).__init__(sprite_grid, x, y)
        self.state = None
        self.sprite_grid = sprite_grid
        self.current_frame = 0
        self.speed = spd
        self.key = KeyStateHandler()
        self.inventory = Inventory()
        self.spawn_position = x, y
        self.win = 0
        self.death = 0
        self._frame_iteration = 0
        self.n_games = 1
        self.gamma = 0.9
        self.epsilon = 0
        # 11 game states , 3 actions
        self.memory = deque(maxlen=MAX_MEMORY)
        # TODO: Change neural network dimensions here
        self.model = Linear_QNet(9, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    # TODO: Change model Linear QNET input size when adding more state variables.
    def get_action(self, state) -> list:

        self.epsilon = 80 - self.n_games

        movement_pattern = [0, 0, 0, 0]

        if np.random.randint(low=0, high=200) < self.epsilon:
            move = np.random.randint(low=0, high=3)
            movement_pattern[move] = 1

        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            movement_pattern[move] = 1

        return movement_pattern

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

    def game_win(self):
        self.x, self.y = self.spawn_position
        self.win += 1

    @property
    def frame_iteration(self):
        return self._frame_iteration

    @frame_iteration.setter
    def frame_iteration(self, value):
        self._frame_iteration = value

    def make_move(self, action):

        if np.array_equal(action, a2=[1, 0, 0, 0]):
            self.x -= self.speed * self.dt

        if np.array_equal(action, a2=[0, 1, 0, 0]):
            ic('going right')
            self.x += self.speed * self.dt

        if np.array_equal(action, a2=[0, 0, 1, 0]):
            ic('going up')
            self.y += self.speed * self.dt

        else:
            ic('going down')
            self.y -= self.speed * self.dt

    def update(self, dt, action):

        self.prev_x = self.x
        self.prev_y = self.y
        self.frame_iteration += dt

        if np.array_equal(action, a2=[1, 0, 0, 0]):
            self.x -= self.speed * dt

        if np.array_equal(action, a2=[0, 1, 0, 0]):
            self.x += self.speed * dt

        if np.array_equal(action, a2=[0, 0, 1, 0]):
            self.y += self.speed * dt

        else:
            self.y -= self.speed * dt

    def die(self):
        self.x, self.y = self.spawn_position
        self.death += 1
        self.inventory.red_key = 0
        self.inventory.blue_key = 0


def train():
    # initialize game
    g = game.GoblinAI(
        **GAME_SPECS.get_window_params(),
        f_screen=False,
        _agent=Agent(**AGENT_PARAMS),
        img_manager=IMAGE_MANAGER,
        puzzle_data=PUZZLE_DATA,
        stage=STAGE_A)

    pyg.clock.schedule_interval(g.update, 1 / 60.0)
    pyg.app.run()

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    # if done:
    #
    #     g.agent.n_games += 1
    #     g.agent.train_long_memory()
    #
    #     # remember
    #     g.agent.remember(state_old, final_move, reward, state_new, done)
    #
    #     if g.game_score > record:
    #         record = g.game_score
    #         g.agent.model.save()
    #
    #     print('game', g.agent.n_games, 'score', g.game_score, 'record', record)
    #     plot_scores.append(g.game_score)
    #     total_score += g.game_score
    #     mean_score = total_score / g.agent.n_games
    #     plot_mean_scores.append(mean_score)
    #     plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
