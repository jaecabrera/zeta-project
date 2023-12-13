from collections import deque
from enum import Enum

import torch
from pyglet.window.key import KeyStateHandler

from game_state import CollisionState
# from game import CollisionState
# from game import GoblinAI
from inventory_system import Inventory
from model import Linear_QNet, QTrainer
from util.common_imports import *

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


# TODO: Create states agent to game. Make sure the return type is of list[`int`]
# the state list is a lot which includes multiple boolean values of the states converted into int
# this includes collisions(box) + mushroom location + door location + spike location
# we need to give danger states to our model for it to learn to avoid
# the reinforcement learning model is a basic model. That's why game states should be clear and simple.

class AgentState(Enum):
    """
    Temporary: (the better solution is to have a function to assert game state to agent rather than
    creating a list of per collision identifiers).
    """
    collision_left = [1, 0, 0, 0]
    collision_right = [1, 0, 0, 0]
    collision_top = [1, 0, 0, 0]
    collision_down = ...
    spike = ...
    door_unlocked = ...
    door_locked = ...


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
        self.n_games = 0
        self.gamma = 0.9
        self.epsilon = 0
        # 11 game states , 3 actions
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, col_state: CollisionState) -> None:
        self.state = [
            col_state.up,
            col_state.down,
            col_state.right,
            col_state.down,
            col_state.nearby_danger,
            col_state.nearby_key,
            col_state.nearby_door
        ]

    def get_action(self) -> pyg.window.key:
        self.epsilon = 80 - self.n_games

        movement_pattern = [0, 0, 0, 0]

        if np.random.randint(0, 200) < self.epsilon:
            move = np.random.randint(0, 3)
            movement_pattern[move] = 1
        else:
            state0 = torch.tensor(self.state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            movement_pattern[move] = 1

        return movement_pattern

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self):
        ...

    def train_long_memory(self):
        ...

    def game_win(self):
        self.x, self.y = self.spawn_position
        self.win += 1

    @property
    def frame_iteration(self):
        return self._frame_iteration

    @frame_iteration.setter
    def frame_iteration(self, value):
        self._frame_iteration = value

    def update(self, dt):

        self.prev_x = self.x
        self.prev_y = self.y

        self.frame_iteration += dt

        if self.left:
            self.x -= self.speed * dt

        if self.right:
            self.x += self.speed * dt

        if self.up:
            self.y += self.speed * dt

        if self.down:
            self.y -= self.speed * dt

    def die(self):
        self.x, self.y = self.spawn_position
        self.death += 1
        self.inventory.red_key = 0
        self.inventory.blue_key = 0


def train():
    ...
    # game = GoblinAI(
    #     **GAME_SPECS.get_window_params(),
    #     f_screen=False,
    #     ai_params=AGENT_PARAMS,
    #     img_manager=IMAGE_MANAGER,
    #     puzzle_data=PUZZLE_DATA,
    #     stage=STAGE_A)

    # old state
    state_old = game.agent.get_state()
#     final_move = agent.get_action(state_old)
#     reward, done, score = game.play_step(final_move)
#     state_new = agent.get_state(game)
#
#     # train short memory
#     agent.train_short_memory(state_old, final_move, reward, state_new, done)
#
#     # remember
#     agent.remember(state_old, final_move, reward, state_new, done)
#
#     # if done
#     game.reset_stage()
#     agent.train_long_memory()
#     agent.n_games += 1
#
#     # if score > record:
#     record = score
#     agent.model.save()
#
#     # etc. etc
