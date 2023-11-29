from pyglet.window.key import KeyStateHandler

from common_imports import *


class Item:

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Inventory:
    def __init__(self):
        self.items = []

    def check_items(self):
        return [i for i in self.items]

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item: Item):
        if item.description in self.items:
            self.items.remove(item)


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
        super(Agent, self).__init__(sprite_grid[0], x, y)
        self.sprite_grid = sprite_grid
        self.current_frame = 0
        self.speed = spd
        self.key = KeyStateHandler()
        self.inventory = Inventory()

    def update(self, dt):

        self.image = self.sprite_grid[self.current_frame]

        if self.left:
            self.x -= self.speed * dt
            self.current_frame = (self.current_frame + 1) % len(self.sprite_grid)

        if self.right:
            self.x += self.speed * dt
            self.current_frame = (self.current_frame + 1) % len(self.sprite_grid)

        if self.up:
            self.y += self.speed * dt
            self.current_frame = (self.current_frame + 1) % len(self.sprite_grid)

        if self.down:
            self.y -= self.speed * dt
            self.current_frame = (self.current_frame + 1) % len(self.sprite_grid)
