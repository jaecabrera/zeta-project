from collections import deque

from pyglet.window.key import KeyStateHandler

from inventory_system import Inventory
from model import Linear_QNet, QTrainer
from util.common_imports import *

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


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
        self.sprite_grid = sprite_grid
        self.current_frame = 0
        self.speed = spd
        self.key = KeyStateHandler()
        self.inventory = Inventory()
        self.spawn_position = x, y
        self.win = 0
        self.death = 0
        self.reward = 0
        self._frame_iteration = 0
        self.gamma = 0.9
        # 11 game states , 3 actions
        self.memory = deque(max_len=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self):
        ...

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self):
        ...

    def train_long_memory(self):
        ...

    def game_win(self):
        self.x, self.y = self.spawn_position
        self.win += 1
        self.reward += 10

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
        self.reward -= 10
        self.inventory.red_key = 0
        self.inventory.blue_key = 0
