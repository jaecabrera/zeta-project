import logging
from pathlib import Path
import pyglet as pyg
from pyglet.window import key, mouse
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

""" Window"""
window_width = 1024
window_height = 768
total_frames = 60

logger.debug(f"width: {window_width}, height: {window_height}, frames: {total_frames}")
window = pyg.window.Window(width=window_width, height=window_height, fullscreen=False)
fps_display = pyg.window.FPSDisplay(window=window)

""" Sprite Sheet """
agent_idle = Path.cwd() / "assets" / "sprite" / "4 Woman" / "Woman_walk.png"
sprite_sheet = pyg.image.load(agent_idle)
num_rows = 1
num_cols = 6
frame_width = sprite_sheet.width // num_cols
frame_height = sprite_sheet.height // num_rows
animation = pyg.image.ImageGrid(sprite_sheet, num_rows, num_cols)
texture_grid = pyg.image.TextureGrid(animation)
sprite = pyg.sprite.Sprite(texture_grid[0])

logging.debug(f"Agent: sheet-width {sprite_sheet.width}, frame-height {sprite_sheet.height}")
logging.debug(f"Agent: frame-width {frame_width}, frame-height {frame_height}")

speed = 90

""" Starting Position """
agent_pos_x = window_width // 2 - frame_width // 2
agent_pos_y = window_height // 2 - frame_height // 2


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

    def update(self, dt):

        self.image = texture_grid[self.current_frame]

        if self.left:
            self.x -= speed * dt
            self.current_frame = (self.current_frame + 1) % len(texture_grid)

        if self.right:
            self.x += speed * dt
            self.current_frame = (self.current_frame + 1) % len(texture_grid)

        if self.up:
            self.y += speed * dt
            self.current_frame = (self.current_frame + 1) % len(texture_grid)

        if self.down:
            self.y -= speed * dt
            self.current_frame = (self.current_frame + 1) % len(texture_grid)


""" Agent Initialized """
agent = Agent(texture_grid, agent_pos_x, agent_pos_y, speed)


def update(dt):
    agent.update(dt)


# Schedule the update function to be called regularly
pyg.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    agent.draw()


@window.event
def on_key_press(symbol, modifiers):
    match symbol:

        case key.W:
            agent.move('up', True)

        case key.A:
            agent.move('left', True)

        case key.S:
            agent.move('down', True)

        case key.D:
            agent.move('right', True)


@window.event
def on_key_release(symbol, modifiers):
    match symbol:

        case key.W:
            agent.move('up', False)

        case key.A:
            agent.move('left', False)

        case key.S:
            agent.move('down', False)

        case key.D:
            agent.move('right', False)

    agent.current_frame = 0


@window.event
def on_mouse_press(x, y, button, modifiers):
    match button:
        case mouse.LEFT:
            print('left button press')
        case mouse.RIGHT:
            print('right button press')


pyg.app.run()