import logging
from pathlib import Path
import numpy as np
import pyglet as pyg
from pyglet.window import key, mouse

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
agent_idle = Path.cwd() / "assets" / "sprite" / "1 Old_man" / "Old_man_walk.png"
sprite_sheet = pyg.image.load(agent_idle)

num_rows = 1
num_cols = 6

frame_width = sprite_sheet.width // num_cols
frame_height = sprite_sheet.height // num_rows

logging.debug(f"Agent: sheet-width {sprite_sheet.width}, frame-height {sprite_sheet.height}")
logging.debug(f"Agent: frame-width {frame_width}, frame-height {frame_height}")

speed = 160
animation = pyg.image.ImageGrid(sprite_sheet, num_rows, num_cols)
texture_sequence = pyg.image.TextureGrid(animation)
logging.debug(texture_sequence[0])
sprite = pyg.sprite.Sprite(texture_sequence[0])
logging.debug(f"sequence: {len(texture_sequence)}")

sprite.x = window_width // 2 - frame_width // 2
sprite.y = window_height // 2 - frame_height // 2

is_moving_left = False
is_moving_right = False


# Define the update function to handle sprite animation and movement
def update(dt):
    global is_moving_left

    # Update the sprite animation based on the elapsed time
    sprite.image = texture_sequence[3]

    if is_moving_left:
        sprite.x -= speed * dt

    if is_moving_right:
        sprite.x += speed * dt


# Schedule the update function to be called regularly
pyg.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    sprite.draw()


@window.event
def on_key_press(symbol, modifiers):
    global is_moving_left
    global is_moving_right

    match symbol:

        case key.A:
            for x in np.arange(1, len(texture_sequence[1:])):
                sprite.image = texture_sequence[x]
                is_moving_left = True

        case key.W:
            print('pressed W')

        case key.S:
            print('pressed S')

        case key.D:
            sprite.image = texture_sequence[3]
            is_moving_right = True


@window.event
def on_key_release(symbol, modifiers):
    global is_moving_left
    global is_moving_right

    match symbol:
        case key.A:
            is_moving_left = False
        case key.W:
            print('pressed W')
        case key.S:
            print('pressed S')
        case key.D:
            is_moving_right = False


@window.event
def on_mouse_press(x, y, button, modifiers):
    match button:
        case mouse.LEFT:
            print('left button press')
        case mouse.RIGHT:
            print('right button press')


pyg.app.run()
