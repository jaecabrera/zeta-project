import json
from dataclasses import field
import configparser
import pyglet.image
# from sprite_variables import *
from util.images import ImageManager
from util.puzzle import PuzzleData, PUZZLE_DATA, PuzzleObject
from util.specs import GameSpecs
import pyglet as pyg
from icecream import ic

""" Wall & Stage """


# wall_filepath = Path.cwd() / "assets" / "sprite" / "wall" / "crate.png"
# wall_image = pyg.image.load(wall_filepath)
#
# box_batch = pyg.graphics.Batch()
# box_sprites = []
# wall = WallGenerator(wall_image, WINDOW_HEIGHT, WINDOW_WIDTH, batch=box_batch)


#
# """ Starting Position """
# agent_pos_x = 32
# agent_pos_y = 32
# set_stage(wall, window, box_batch, structure='stage_1')
#

# ------ GAME CLASS


# ---------------------------- GAME OBJECTS --------------------------------------------

# # Doors
# def respawn_objects(pos: list[tuple], data: PuzzleData, object_list: list[PuzzleObject]):
#     object_list += [PuzzleObject(x, y, data) for x, y in pos]
#
#
# # create blue doors - puzzle data
# door_blue_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door_blue.png"
# blue_door_image = pyg.image.load(door_blue_filepath)
# blue_door_pos: list[tuple] = [(32 * 16, 32 * 12), (32 * 8, 32)]
# blue_door_data = PuzzleData(puzzle_type="door", ref_color="blue", image=blue_door_image)
# blue_door_data.create_batch()
# blue_door_list = [PuzzleObject(x, y, blue_door_data) for x, y in blue_door_pos]
#
# # create red doors - puzzle data
# red_door_filepath = Path.cwd() / "assets" / "sprite" / "door" / "door.png"
# red_door_image = pyg.image.load(red_door_filepath)
# red_door_pos: list[tuple] = [
#     (32 * 7, 32 * 11),
#     (32 * 7, 32 * 18)
# ]
# red_door_data = PuzzleData(puzzle_type="door", ref_color="red", image=red_door_image)
# red_door_data.create_batch()
# red_door_list = [PuzzleObject(x, y, red_door_data) for x, y in red_door_pos]
#
# # Mushrooms
#
# red_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "red_mush.png"
# red_shroom_image = pyg.image.load(red_shroom_fp)
# red_shroom_pos: list[tuple] = [(82, 472), (82, 280)]
# red_shroom_data = PuzzleData(puzzle_type="key", ref_color="red", image=red_shroom_image)
# red_shroom_data.create_batch()
# red_shroom_list = [PuzzleObject(x, y, red_shroom_data) for x, y in red_shroom_pos]
#
# blue_shroom_fp = Path.cwd() / "assets" / "sprite" / "shroom" / "blue_mush.png"
# blue_shroom_image = pyg.image.load(blue_shroom_fp)
# blue_shroom_pos: list[tuple] = [(76, 668), (182, 98)]
# blue_shroom_data = PuzzleData(puzzle_type="key", ref_color="blue", image=blue_shroom_image)
# blue_shroom_data.create_batch()
# blue_shroom_list = [PuzzleObject(x, y, blue_shroom_data) for x, y in blue_shroom_pos]
#
# # trap
# trap_sprite_fp = Path.cwd() / "assets" / "sprite" / "trap" / "spike.png"
# trap_image = pyg.image.load(trap_sprite_fp)
# trap_pos: list[tuple] = [(PIXEL * i, 190) for i in np.arange(9, 12, step=1)]
# [trap_pos.append((PIXEL * x, 190)) for x in np.arange(13, 16, step=1)]
# [trap_pos.append((PIXEL * x, PIXEL * 9)) for x in np.arange(9, 15, step=1)]
#
# trap_data = PuzzleData(puzzle_type="trap", ref_color="None", image=trap_image)
# trap_data.create_batch()
# trap_list = [PuzzleObject(x, y, trap_data) for x, y in trap_pos]
#
# """ Agent Initialized """
# agent = Agent(texture_grid, agent_pos_x, agent_pos_y, speed)
#
# # flag
# flag_filepath = Path.cwd() / "assets" / "sprite" / "finish_flag" / "flag.png"
# flag_sheet = pyg.image.load(flag_filepath)
# num_rows = 1
# num_cols = 6
# # frame_width = flag_sheet.width // num_cols
# # frame_height = flag_sheet.height // num_rows
# flag_animation = pyg.image.ImageGrid(flag_sheet, num_rows, num_cols)
# texture_grid = pyg.image.TextureGrid(flag_animation)
# flag_animation_frames = [pyglet.image.AnimationFrame(img, 0.1) for img in flag_animation]
#
# # Create an Animation from the frames
# flag_animation = pyglet.image.Animation(flag_animation_frames)
#
# # Create a Sprite using the Animation
# flag_sprite = pyglet.sprite.Sprite(flag_animation, 570, 396)
#
# inventory_label = pyglet.text.Label(
#     text=f'Red: {0} Blue: {0} / Win: {0} Death: {0} frame-iter: {0}',
#     x=window_width - 50,
#     y=window.height - 50,
#     anchor_x='right',
#     anchor_y='center',
# )
#
#
# def check_collision(sprite1, sprite2):
#     """
#     Basic collision detection based on sprite dimensions.
#     :param sprite1: Sprite A
#     :param sprite2: Sprite B
#     """
#     return (
#             sprite1.x < sprite2.x + sprite2.width and
#             sprite1.x + sprite1.width > sprite2.x and
#             sprite1.y < sprite2.y + sprite2.height and
#             sprite1.y + sprite1.height > sprite2.y
#     )
#
#
# def reset_stage():
#     blue_door_list.clear()
#     red_door_list.clear()
#     red_shroom_list.clear()
#     blue_shroom_list.clear()
#
#     respawn_objects(blue_door_pos, blue_door_data, blue_door_list)
#     respawn_objects(red_door_pos, red_door_data, red_door_list)
#     respawn_objects(red_shroom_pos, red_shroom_data, red_shroom_list)
#     respawn_objects(blue_shroom_pos, blue_shroom_data, blue_shroom_list)
#
#
# def update(dt):
#     # set agent previous x, y pos before agent update
#     agent.prev_x = agent.x
#     agent.prev_y = agent.y
#     previous_reward = agent.reward
#
#     agent.update(dt)
#     agent.frame_iteration += dt
#
#     if (agent.frame_iteration >= 60) & (agent.reward == 0):
#         agent.die()
#         reset_stage()
#         agent.frame_iteration = 0
#
#     if (agent.frame_iteration >= 60) & (agent.reward == previous_reward):
#         agent.die()
#         reset_stage()
#         agent.frame_iteration = 0
#
#     inventory_red, inventory_blue = agent.inventory.red_key, agent.inventory.blue_key
#
#     def update_inventory_count():
#         inventory_label.text = f"""
#     Red: {inventory_red} Blue: {inventory_blue} / Win: {agent.win} / Death: {agent.death}
#     frame-iter: {agent.frame_iteration:.0f} / Reward: {agent.reward} """
#
#     update_inventory_count()
#     for boxes in wall.box_sprites:
#         "Agent bump into box by reverting agent pos to previous pos."
#         if check_collision(agent, boxes):
#             agent.x = agent.prev_x
#             agent.y = agent.prev_y
#
#     for traps in trap_list:
#         if check_collision(agent, traps):
#             agent.die()
#             agent.reward -= 10
#             agent.frame_iteration = 0
#             reset_stage()
#
#     for r_shroom in red_shroom_list:
#         "Red shroom / key is added to inventory when agent collides with shroom"
#         if check_collision(agent, r_shroom):
#             red_shroom_list.remove(r_shroom)
#             agent.inventory.add_red()
#             agent.reward += 10
#
#     for b_shroom in blue_shroom_list:
#         "Blue shroom / key is added to inventory when agent collides with shroom"
#         if check_collision(agent, b_shroom):
#             blue_shroom_list.remove(b_shroom)
#             agent.inventory.add_blue()
#             agent.reward += 10
#
#     for r_door in red_door_list:
#         "Check if agent has a red key, if true then removes red door and deducts red total key."
#         if agent.inventory.red_key != 0:
#
#             if check_collision(agent, r_door):
#                 red_door_list.remove(r_door)
#                 agent.inventory.minus_red()
#
#         elif check_collision(agent, r_door):
#             agent.x = agent.prev_x
#             agent.y = agent.prev_y
#
#     for b_door in blue_door_list:
#         "Check if agent has a blue key, if true then removes blue door and deducts blue total key."
#         if agent.inventory.blue_key != 0:
#
#             if check_collision(agent, b_door):
#                 blue_door_list.remove(b_door)
#                 agent.inventory.minus_blue()
#
#         elif check_collision(agent, b_door):
#             agent.x = agent.prev_x
#             agent.y = agent.prev_y
#
#     if check_collision(agent, flag_sprite):
#         agent.game_win()
#         agent.x, agent.y = agent.spawn_position
#
#         reset_stage()
#
#
# # Schedule the update function to be called regularly
# pyg.clock.schedule_interval(update, 1 / 60.0)
#
#
# @window.event
# def on_draw():
#     window.clear()
#     background_image.blit(0, 0)
#     flag_sprite.draw()
#     red_shroom_data.batch.draw()
#     blue_shroom_data.batch.draw()
#     trap_data.batch.draw()
#     agent.draw()
#     box_batch.draw()
#     red_door_data.batch.draw()
#     blue_door_data.batch.draw()
#     trap_data.batch.draw()
#     inventory_label.draw()
#     fps_display.draw()
#
#
# @window.event
# def on_key_press(symbol, modifiers):
#     match symbol:
#
#         case key.W:
#             agent.move(direction='up', state=True)
#
#         case key.A:
#             agent.move(direction='left', state=True)
#
#         case key.S:
#             agent.move(direction='down', state=True)
#
#         case key.D:
#             agent.move(direction='right', state=True)
#
#         case key.V:
#             ic(agent.x, agent.y)
#
#         case key.F:
#             agent.speed += 32
#
#         case key.R:
#             agent.speed -= 32
#
#         case key.G:
#             agent.speed = DEFAULT_SPEED
#
#         case key.M:
#             ic(agent.inventory.blue_key, agent.inventory.red_key)
#
#
# @window.event
# def on_key_release(symbol, modifiers):
#     match symbol:
#
#         case key.W:
#             agent.move('up', False)
#
#         case key.A:
#             agent.move('left', False)
#
#         case key.S:
#             agent.move('down', False)
#
#         case key.D:
#             agent.move('right', False)


class GoblinAI(pyg.window.Window):

    def __init__(self, width: int, height: int, f_screen: bool, ai_params: dict, img_manager: ImageManager,
                 puzzle_data, stage) -> None:
        super().__init__(width, height, fullscreen=f_screen)
        self.blue_door_list = []
        self.red_door_list = []
        self.red_mushroom_list = []
        self.blue_mushroom_list = []
        self.trap_list = []
        self.box_list = []
        self.loaded_puzzle_data = None
        self.puzzle_blue_shroom = None
        self.puzzle_red_shroom = None
        self.puzzle_trap = None
        self.puzzle_blue_door = None
        self.puzzle_red_door = None
        self.puzzle_crate = None
        self.image_manager = img_manager
        self.game_images = None
        self.puzzle_data = puzzle_data
        self.stage = stage
        self.__post_init__()

        # self.agent = Agent(**ai_params)

    def __post_init__(self):
        self.retrieve_pyglet_images()
        self.make_puzzle_data(self.puzzle_data)
        self.place_puzzle_objects(self.stage)

    def retrieve_pyglet_images(self):
        self.game_images = self.image_manager.pyglet_images

    def make_puzzle_data(self, puzzle_data: dict):

        puzzle_data.get('b').image = self.image_manager.pyglet_images.get('crate_image')
        self.puzzle_crate = puzzle_data.get('b')
        self.puzzle_crate.create_batch()

        puzzle_data.get('rd').image = self.image_manager.pyglet_images.get('door_red_image')
        self.puzzle_red_door = puzzle_data.get('rd')
        self.puzzle_red_door.create_batch()

        puzzle_data.get('bd').image = self.image_manager.pyglet_images.get('door_blue_image')
        self.puzzle_blue_door = puzzle_data.get('bd')
        self.puzzle_blue_door.create_batch()

        puzzle_data.get('sp').image = self.image_manager.pyglet_images.get('trap_image')
        self.puzzle_trap = puzzle_data.get('sp')
        self.puzzle_trap.create_batch()

        puzzle_data.get('rs').image = self.image_manager.pyglet_images.get('mushroom_red_image')
        self.puzzle_red_shroom = puzzle_data.get('rs')
        self.puzzle_red_shroom.create_batch()

        puzzle_data.get('bs').image = self.image_manager.pyglet_images.get('mushroom_blue_image')
        self.puzzle_blue_shroom = puzzle_data.get('bs')
        self.puzzle_blue_shroom.create_batch()

        self.loaded_puzzle_data = [
            self.puzzle_crate,
            self.puzzle_red_door,
            self.puzzle_blue_door,
            self.puzzle_trap,
            self.puzzle_red_shroom,
            self.puzzle_blue_shroom
        ]

    def place_puzzle_objects(self, stage: dict):
        for k in stage.keys():
            stage.get(k)
            tuple_stage_puzzle = [tuple(x) for x in stage.get(k)]

            match k:
                case 'b':
                    for x, y in tuple_stage_puzzle:
                        self.box_list.append(PuzzleObject(x, y, self.puzzle_crate))

            match k:
                case 'sp':
                    for x, y in tuple_stage_puzzle:
                        self.trap_list.append(PuzzleObject(x, y, self.puzzle_trap))

            match k:
                case 'bs':
                    for x, y in tuple_stage_puzzle:
                        self.blue_mushroom_list.append(PuzzleObject(x, y, self.puzzle_blue_shroom))

            match k:
                case 'rs':
                    for x, y in tuple_stage_puzzle:
                        self.red_mushroom_list.append(PuzzleObject(x, y, self.puzzle_red_shroom))

            match k:
                case 'rd':
                    for x, y in tuple_stage_puzzle:
                        self.red_door_list.append(PuzzleObject(x, y, self.puzzle_red_door))

            match k:
                case 'bd':
                    for x, y in tuple_stage_puzzle:
                        self.blue_door_list.append(PuzzleObject(x, y, self.puzzle_blue_door))

    def on_draw(self):

        self.clear()
        self.puzzle_crate.batch.draw()
        self.puzzle_trap.batch.draw()
        self.puzzle_blue_shroom.batch.draw()
        self.puzzle_red_shroom.batch.draw()
        self.puzzle_red_door.batch.draw()
        self.puzzle_blue_door.batch.draw()

    def on_key_press(self, symbol, modifiers):
        ...

    def on_key_release(self, symbol, modifiers):
        ...


if __name__ == '__main__':
    with open('puzzle_objects.json', 'r') as f:
        STAGE_A = json.load(f)

    # Config
    config = configparser.ConfigParser()
    config.read('config.ini')
    relative_image_fp = {k: config['PATHS'][v] for k, v in zip(config['PATHS'], config['PATHS'])}

    # Game and Image Managers
    image_manager = ImageManager(relative_image_fp)
    game_params = GameSpecs()
    image_manager.load_pyglet_images()

    game = GoblinAI(
        **game_params.get_window_params(),
        f_screen=False,
        ai_params=dict(),
        img_manager=image_manager,
        puzzle_data=PUZZLE_DATA,
        stage=STAGE_A)

    pyglet.app.run()
