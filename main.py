import logging

from icecream import ic
from pyglet import gl

from common_imports import *
from machine import Agent
from stage import WallGenerator

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

""" Window 1024 x 768 """
window_width = 1024
window_height = 768
total_frames = 60

logger.debug(f"width: {window_width}, height: {window_height}, frames: {total_frames}")
window = pyg.window.Window(width=window_width, height=window_height, fullscreen=False)
fps_display = pyg.window.FPSDisplay(window=window)
gl.glClearColor(.31, .08, .08, 1.0)

""" Sprite Sheet """
agent_idle = Path.cwd() / "assets" / "sprite" / "bot" / "bot.png"
sprite_sheet = pyg.image.load(agent_idle)
num_rows = 1
num_cols = 1
frame_width = sprite_sheet.width // num_cols
frame_height = sprite_sheet.height // num_rows
animation = pyg.image.ImageGrid(sprite_sheet, num_rows, num_cols)
texture_grid = pyg.image.TextureGrid(animation)
sprite = pyg.sprite.Sprite(texture_grid[0])

logging.debug(f"Agent: sheet-width {sprite_sheet.width}, frame-height {sprite_sheet.height}")
logging.debug(f"Agent: frame-width {frame_width}, frame-height {frame_height}")

DEFAULT_SPEED = 200
speed = DEFAULT_SPEED
""" Starting Position """
agent_pos_x = 32
agent_pos_y = 32

# TODO: Create boundary box function

wall_filepath = Path.cwd() / "assets" / "sprite" / "wall" / "crate.png"
wall_image = pyg.image.load(wall_filepath)

box_batch = pyg.graphics.Batch()
box_sprites = []

wall = WallGenerator(wall_image, window_height, window_width, batch=box_batch)

for i in np.arange(32, 768 // 2, step=32):
    wall.generate_box(window.width // 2, y=i, batch=box_batch)

for i in np.arange(768 // 2 + 32, 768, step=32):
    wall.generate_box(window.width // 2, y=i, batch=box_batch)

for i in np.arange(window_width // 4, step=32):
    wall.generate_box(x=i, y=window_height // 4, batch=box_batch)

for i in np.arange(window_width // 4, step=32):
    wall.generate_box(x=i, y=window_height // 4, batch=box_batch)

for i in np.arange(window_height // 4, window_height // 2, step=32):
    wall.generate_box(x=window_width // 4, y=i, batch=box_batch)

for i in np.arange(32 * 14, 768, step=32):
    wall.generate_box(x=window_width // 4, y=i, batch=box_batch)

for i in np.arange(32, window_width // 4 - 32, step=32):
    wall.generate_box(x=i, y=32 * 11, batch=box_batch)

for i in np.arange(32, window_width // 4 - 32, step=32):
    wall.generate_box(x=i, y=32 * 18, batch=box_batch)

# TODO: Create door class (blit or destroy when key is in inventory.)

door_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door.png"
door_image = pyg.image.load(door_filepath)
door_batch = []


class Door(pyg.sprite.Sprite):

    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.image = image


door = Door(door_image, x=32 * 7, y=32 * 11)

# TODO: Create key/key card class
""" Agent Initialized """
agent = Agent(texture_grid, agent_pos_x, agent_pos_y, speed)


def check_collision(sprite1, sprite2):
    return (
            sprite1.x < sprite2.x + sprite2.width and
            sprite1.x + sprite1.width > sprite2.x and
            sprite1.y < sprite2.y + sprite2.height and
            sprite1.y + sprite1.height > sprite2.y
    )


def update(dt):
    # collision: store previous player position.
    agent.prev_x = agent.x
    agent.prev_y = agent.y

    agent.update(dt)

    for boxes in wall.box_sprites:
        if check_collision(agent, boxes):
            agent.x = agent.prev_x
            agent.y = agent.prev_y


# Schedule the update function to be called regularly
pyg.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    agent.draw()
    box_batch.draw()
    door.draw()


@window.event
def on_key_press(symbol, modifiers):
    # ic(agent.x, agent.y, wall.x, wall.y)
    match symbol:

        case key.W:
            agent.move('up', True)

        case key.A:
            agent.move('left', True)

        case key.S:
            agent.move('down', True)

        case key.D:
            agent.move('right', True)

        case key.V:
            ic(agent.x, agent.y)
        # case key.F:
        #     agent.speed += 32
        #
        # case key.R:
        #     agent.speed -= 32
        #
        # case key.G:
        #     agent.speed = DEFAULT_SPEED


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
