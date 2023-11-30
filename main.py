from icecream import ic
from pyglet import gl

from common_imports import *
from agent import Agent
from stage import WallGenerator, set_stage
from puzzle import PuzzleData, PuzzleObject

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

""" Speed Params """
DEFAULT_SPEED = 200
speed = DEFAULT_SPEED

""" Starting Position """
agent_pos_x = 32
agent_pos_y = 32

""" Wall & Stage """
wall_filepath = Path.cwd() / "assets" / "sprite" / "wall" / "crate.png"
wall_image = pyg.image.load(wall_filepath)

box_batch = pyg.graphics.Batch()
box_sprites = []
wall = WallGenerator(wall_image, window_height, window_width, batch=box_batch)
set_stage(wall, window, box_batch, structure='stage_1')

# Doors

# create blue doors - puzzle data
door_blue_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door_blue.png"
blue_door_image = pyg.image.load(door_blue_filepath)
blue_door_pos: list[tuple] = [(32 * 16, 32 * 12)]
blue_door_data = PuzzleData(puzzle_type="door", ref_color="blue", image=blue_door_image)
blue_door_data.create_batch()
blue_door_list = [PuzzleObject(x, y, blue_door_data) for x, y in blue_door_pos]

# create red doors - puzzle data
red_door_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door.png"
red_door_image = pyg.image.load(red_door_filepath)
red_door_pos: list[tuple] = [
    (32 * 7, 32 * 11),
    (32 * 7, 32 * 18)
]
red_door_data = PuzzleData(puzzle_type="door", ref_color="red", image=red_door_image)
red_door_data.create_batch()
red_door_list = [PuzzleObject(x, y, red_door_data) for x, y in red_door_pos]

# Mushrooms

red_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "red_mush.png"
red_shroom_image = pyg.image.load(red_shroom_fp)
red_shroom_pos: list[tuple] = [(82, 472), (82, 280)]
red_shroom_data = PuzzleData(puzzle_type="key", ref_color="red", image=red_shroom_image)
red_shroom_data.create_batch()
red_shroom_list = [PuzzleObject(x, y, red_shroom_data) for x, y in red_shroom_pos]

blue_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "blue_mush.png"
blue_shroom_image = pyg.image.load(blue_shroom_fp)
blue_shroom_pos: list[tuple] = [(76, 668)]
blue_shroom_data = PuzzleData(puzzle_type="key", ref_color="blue", image=blue_shroom_image)
blue_shroom_data.create_batch()
blue_shroom_list = [PuzzleObject(x, y, blue_shroom_data) for x, y in blue_shroom_pos]

""" Agent Initialized """
agent = Agent(texture_grid, agent_pos_x, agent_pos_y, speed)


def check_collision(sprite1, sprite2):
    """
    Basic collision detection based on sprite dimensions.
    :param sprite1: Sprite A
    :param sprite2: Sprite B
    """
    return (
            sprite1.x < sprite2.x + sprite2.width and
            sprite1.x + sprite1.width > sprite2.x and
            sprite1.y < sprite2.y + sprite2.height and
            sprite1.y + sprite1.height > sprite2.y
    )


def update(dt):
    # set agent previous x, y pos before agent update
    agent.prev_x = agent.x
    agent.prev_y = agent.y

    agent.update(dt)

    for boxes in wall.box_sprites:
        "Agent bump into box by reverting agent pos to previous pos."
        if check_collision(agent, boxes):
            agent.x = agent.prev_x
            agent.y = agent.prev_y

    for r_shroom in red_shroom_list:
        "Red shroom / key is added to inventory when agent collides with shroom"
        if check_collision(agent, r_shroom):
            red_shroom_list.remove(r_shroom)
            agent.inventory.add_red()

    for b_shroom in blue_shroom_list:
        "Blue shroom / key is added to inventory when agent collides with shroom"
        if check_collision(agent, b_shroom):
            blue_shroom_list.remove(b_shroom)
            agent.inventory.add_blue()

    for r_door in red_door_list:
        "Check if agent has a red key, if true then removes red door and deducts red total key."
        if agent.inventory.red_key != 0:

            if check_collision(agent, r_door):
                red_door_list.remove(r_door)
                agent.inventory.minus_red()

        elif check_collision(agent, r_door):
            agent.x = agent.prev_x
            agent.y = agent.prev_y

    for b_door in blue_door_list:
        "Check if agent has a blue key, if true then removes blue door and deducts blue total key."
        if agent.inventory.blue_key != 0:

            if check_collision(agent, b_door):
                blue_door_list.remove(b_door)
                agent.inventory.minus_blue()

        elif check_collision(agent, b_door):
            agent.x = agent.prev_x
            agent.y = agent.prev_y


# Schedule the update function to be called regularly
pyg.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    window.clear()
    red_shroom_data.batch.draw()
    blue_shroom_data.batch.draw()
    agent.draw()
    box_batch.draw()
    red_door_data.batch.draw()
    blue_door_data.batch.draw()
    fps_display.draw()


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

        case key.V:
            ic(agent.x, agent.y)

        case key.F:
            agent.speed += 32

        case key.R:
            agent.speed -= 32

        case key.G:
            agent.speed = DEFAULT_SPEED

        case key.M:
            ic(agent.inventory.blue_key, agent.inventory.red_key)


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


if __name__ == '__main__':
    pyg.app.run()
