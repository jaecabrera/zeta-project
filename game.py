import configparser
import json
from pathlib import Path

import pyglet as pyg
import pyglet.image
from icecream import ic
from pyglet.window import key

from agent import Agent
from util.images import ImageManager
from util.puzzle import PUZZLE_DATA, PuzzleObject
from util.specs import GameSpecs


# TODO: create game win flag on: self.agent.x: 126.66783997416496, self.agent.y: 375.9084399426356
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
        self.flag_finish = None
        self.loaded_puzzle_data = None
        self.puzzle_blue_shroom = None
        self.puzzle_red_shroom = None
        self.puzzle_trap = None
        self.puzzle_blue_door = None
        self.puzzle_red_door = None
        self.puzzle_crate = None
        self.image_manager = img_manager
        self.game_images = None
        self.game_stats = None
        self.puzzle_data = puzzle_data
        self.stage = stage
        self.__post_init__()
        self.agent = Agent(**ai_params)

    def __post_init__(self):
        self.retrieve_pyglet_images()
        self.make_puzzle_data(self.puzzle_data)
        self.place_puzzle_objects(self.stage)
        self.make_game_stats_label()

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

            flag_animated = self.set_flag()
            self.flag_finish = pyglet.sprite.Sprite(flag_animated, 70, 350)

    def set_flag(self):

        flag_image = self.image_manager.pyglet_images.get('flag_image')
        flag_image_animation = pyg.image.ImageGrid(flag_image, 1, 6)
        flag_texture_grid = pyg.image.TextureGrid(flag_image_animation)
        flag_animated = [pyglet.image.AnimationFrame(img, 0.1) for img in flag_texture_grid]
        flag_image_obj = pyglet.image.Animation(flag_animated)
        return flag_image_obj

    def make_game_stats_label(self):
        self.game_stats = pyglet.text.Label(
            text='',
            x=self.width - 50,
            y=self.height - 50,
            anchor_x='right',
            anchor_y='center',
        )

    def on_draw(self):

        self.clear()
        self.agent.draw()
        self.flag_finish.draw()
        self.game_stats.draw()
        self.puzzle_crate.batch.draw()
        self.puzzle_trap.batch.draw()
        self.puzzle_blue_shroom.batch.draw()
        self.puzzle_red_shroom.batch.draw()
        self.puzzle_red_door.batch.draw()
        self.puzzle_blue_door.batch.draw()

    def on_key_press(self, symbol, modifiers):
        match symbol:

            case key.W:
                self.agent.move(direction='up', state=True)

            case key.A:
                self.agent.move(direction='left', state=True)

            case key.S:
                self.agent.move(direction='down', state=True)

            case key.D:
                self.agent.move(direction='right', state=True)

            case key.V:
                ic(self.agent.x, self.agent.y)

    def on_key_release(self, symbol, modifiers):

        match symbol:

            case key.W:
                self.agent.move(direction='up', state=False)

            case key.A:
                self.agent.move(direction='left', state=False)

            case key.S:
                self.agent.move(direction='down', state=False)

            case key.D:
                self.agent.move(direction='right', state=False)

    def check_collision(self, sprite2):
        """
        Basic collision detection based on sprite dimensions.
        :param sprite2: Sprite B
        """
        return (
                self.agent.x < sprite2.x + sprite2.width and
                self.agent.x + self.agent.width > sprite2.x and
                self.agent.y < sprite2.y + sprite2.height and
                self.agent.y + self.agent.height > sprite2.y
        )

    def reset_stage(self):

        self.blue_door_list.clear()
        self.red_door_list.clear()
        self.red_mushroom_list.clear()
        self.blue_mushroom_list.clear()
        self.box_list.clear()
        self.trap_list.clear()

        self.place_puzzle_objects(self.stage)

    def update(self, dt):
        self.agent.update(dt)
        previous_reward = self.agent.reward
        self.game_stats.text = f"""
        Red: {self.agent.inventory.red_key} Blue: {self.agent.inventory.blue_key} 
        Win: {self.agent.win} / Death: {self.agent.death}
        frame-iter: {self.agent.frame_iteration:.0f} / Reward: {self.agent.reward} """

        if (self.agent.frame_iteration >= 60) & (self.agent.reward == 0):
            self.agent.die()
            self.reset_stage()
            self.agent.frame_iteration = 0

        if (self.agent.frame_iteration >= 60) & (self.agent.reward == previous_reward):
            self.agent.die()
            self.reset_stage()
            self.agent.frame_iteration = 0

        for crates in self.box_list:
            if self.check_collision(crates):
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        for traps in self.trap_list:
            if self.check_collision(traps):
                self.agent.die()
                self.agent.reward -= 10
                self.agent.frame_iteration = 0
                self.reset_stage()

        for r_shroom in self.red_mushroom_list:
            "Red shroom / key is added to inventory when agent collides with shroom"
            if self.check_collision(r_shroom):
                self.red_mushroom_list.remove(r_shroom)
                self.agent.inventory.add_red()
                self.agent.reward += 10

        for b_shroom in self.blue_mushroom_list:
            "Blue shroom / key is added to inventory when agent collides with shroom"
            if self.check_collision(b_shroom):
                self.blue_mushroom_list.remove(b_shroom)
                self.agent.inventory.add_blue()
                self.agent.reward += 10

        for r_door in self.red_door_list:
            "Check if agent has a red key, if true then removes red door and deducts red total key."
            if self.agent.inventory.red_key != 0:

                if self.check_collision(r_door):
                    self.red_door_list.remove(r_door)
                    self.agent.inventory.minus_red()

            elif self.check_collision(r_door):
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        for b_door in self.blue_door_list:
            "Check if self.agent has a blue key, if true then removes blue door and deducts blue total key."
            if self.agent.inventory.blue_key != 0:

                if self.check_collision(b_door):
                    self.blue_door_list.remove(b_door)
                    self.agent.inventory.minus_blue()

            elif self.check_collision(b_door):
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        if self.check_collision(self.flag_finish):
            self.agent.game_win()
            self.agent.frame_iteration = 0
            self.reset_stage()


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

    agent_img_fp = Path.cwd() / "assets" / "sprite" / "bot" / "bot.gif"
    animation = pyg.image.load_animation(agent_img_fp)
    sprite = pyg.sprite.Sprite(animation)

    test_agent_params = {
        'sprite_grid': animation,
        'x': 64,
        'y': 64,
        'spd': 120,
    }

    game = GoblinAI(
        **game_params.get_window_params(),
        f_screen=False,
        ai_params=test_agent_params,
        img_manager=image_manager,
        puzzle_data=PUZZLE_DATA,
        stage=STAGE_A)

    pyg.clock.schedule_interval(game.update, 1 / 60.0)
    pyglet.app.run()
