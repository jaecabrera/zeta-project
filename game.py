from dataclasses import dataclass, field

import numpy as np
import pyglet as pyg
import pyglet.image
from icecream import ic
from pyglet.window import key

from agent import Agent
from loader import STAGE_A, IMAGE_MANAGER, AGENT_PARAMS, GAME_SPECS
from util.images import ImageManager
from util.puzzle import PUZZLE_DATA, PuzzleObject

GAME_WIN: bool = False


@dataclass(slots=True, frozen=True)
class ScoreRecords:
    door_counts: int
    key_counts: int


@dataclass
class CollisionState:
    left: bool = field(default=False)
    right: bool = field(default=False)
    up: bool = field(default=False)
    down: bool = field(default=False)
    nearby_door: bool = field(default=False)
    nearby_key: bool = field(default=False)
    nearby_danger: bool = field(default=False)


class GoblinAI(pyg.window.Window):

    def __init__(self, width: int, height: int, f_screen: bool, ai_params: dict, img_manager: ImageManager,
                 puzzle_data, stage, state) -> None:
        super().__init__(width, height, fullscreen=f_screen)
        self.game_score_record = None
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
        self.state = CollisionState()
        self.__post_init__()
        self.agent = Agent(**ai_params)
        self.reward = 0
        self.game_score = 0

    def __post_init__(self):
        self.retrieve_pyglet_images()
        self.make_puzzle_data(self.puzzle_data)
        self.place_puzzle_objects(self.stage)
        self.make_game_stats_label()
        self.store_total_puzzle_objects()

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

    def check_collision(self, game_obj):
        """
        Basic collision detection based on sprite dimensions.
        :param game_obj: Sprite B
        """
        return (
                self.agent.x < game_obj.x + game_obj.width and
                self.agent.x + self.agent.width > game_obj.x and
                self.agent.y < game_obj.y + game_obj.height and
                self.agent.y + self.agent.height > game_obj.y
        )

    def reset_stage(self):

        self.blue_door_list.clear()
        self.red_door_list.clear()
        self.red_mushroom_list.clear()
        self.blue_mushroom_list.clear()
        self.box_list.clear()
        self.trap_list.clear()

        self.place_puzzle_objects(self.stage)

    def _move(self, action):

        if np.array_equal(action, [1, 0, 0, 0]):
            ...

    def store_total_puzzle_objects(self) -> None:
        """
        Counts the remaining puzzle objects in stage such as keys, and doors. This function
        is a utility function for scoring.
        """

        total_mushrooms: int
        total_doors: int

        total_mushrooms = len(self.red_mushroom_list) + len(self.blue_mushroom_list)
        total_doors = len(self.red_door_list) + len(self.blue_door_list)
        self.game_score_record = ScoreRecords(total_doors, total_mushrooms)

    def calculate_total_stage_score(self) -> None:
        """
        :rtype None:
        """
        global GAME_WIN

        def get_total_puzzle_objects() -> tuple:
            """Gets the total puzzle objects from a ScoreRecords Class or self.game_score_records"""
            total_doors = self.game_score_record.door_counts
            total_keys = self.game_score_record.key_counts

            return total_doors, total_keys

        def calculate_completion_score(total_puzzle_objects: tuple) -> int:
            """
            Get the difference in puzzle objects and uses a constant to weight
            priority in scoring which is key > door.
            :param total_puzzle_objects:
            :return: returns the sum score of key and door.
            :rtype int:
            """
            door_const = .1
            key_const = .25

            total_doors, total_keys = total_puzzle_objects
            current_doors = len(self.red_door_list) + len(self.blue_door_list)
            current_keys = len(self.red_mushroom_list) + len(self.blue_mushroom_list)

            door_diff = current_doors - total_doors
            key_diff = current_keys - total_keys
            door_completion_score = np.sum([x * 100 * door_const for x in np.arange(np.abs(door_diff))])
            key_completion_score = np.sum([x * 100 * key_const for x in np.arange(np.abs(key_diff))])
            completion_score: int = int(door_completion_score) + int(key_completion_score)
            return completion_score

        def calculate_game_score(stage_success_score: int | None) -> int:

            total_puzzle_objects: tuple = get_total_puzzle_objects()
            puzzle_completion_score = calculate_completion_score(total_puzzle_objects)
            if GAME_WIN:
                _game_score: int = stage_success_score + puzzle_completion_score
                return _game_score
            else:
                return puzzle_completion_score

        def get_success_score():
            success_score: int = 0

            if self.agent.frame_iteration > 35:
                success_score += 300

            elif (self.agent.frame_iteration < 35) | (self.agent.frame_iteration >= 24):
                success_score += 600

            elif self.agent.frame_iteration < 24:
                success_score += 1000

            return success_score

        _success_score = get_success_score()
        game_score = calculate_game_score(_success_score)
        ic(_success_score)
        self.game_score += game_score
        ic(self.game_score)

    def game_end(self):

        self.agent.die()
        self.calculate_total_stage_score()
        self.reset_stage()
        self.agent.frame_iteration = 0
        self.game_score = 0

    def update(self, dt):
        global GAME_WIN

        self.agent.update(dt)
        previous_reward = self.reward
        self.game_stats.text = f"""
        Red: {self.agent.inventory.red_key} Blue: {self.agent.inventory.blue_key} 
        Win: {self.agent.win} / Death: {self.agent.death}
        Score: {self.game_score} / Reward: {self.reward}
        Seconds: {self.agent.frame_iteration:0.2f}"""

        if (self.agent.frame_iteration >= 60) & (self.reward == 0):
            self.agent.die()
            self.game_end()
            self.reward -= 10

        if (self.agent.frame_iteration >= 60) & (self.reward == previous_reward):
            self.agent.die()
            self.game_end()
            self.reward -= 10

        for crates in self.box_list:
            if self.check_collision(crates):
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        for traps in self.trap_list:
            if self.check_collision(traps):
                self.agent.die()
                self.game_end()
                self.reward -= 10

        for r_shroom in self.red_mushroom_list:
            "Red shroom / key is added to inventory when agent collides with shroom"
            if self.check_collision(r_shroom):
                self.red_mushroom_list.remove(r_shroom)
                self.agent.inventory.add_red()
                self.reward += 10
                self.game_score += 50

        for b_shroom in self.blue_mushroom_list:
            "Blue shroom / key is added to inventory when agent collides with shroom"
            if self.check_collision(b_shroom):
                self.reward += 10
                self.game_score += 50
                self.blue_mushroom_list.remove(b_shroom)
                self.agent.inventory.add_blue()

        for r_door in self.red_door_list:
            "Check if agent has a red key, if true then removes red door and deducts red total key."
            if self.agent.inventory.red_key != 0:

                if self.check_collision(r_door):
                    self.reward += 5
                    self.game_score += 10
                    self.red_door_list.remove(r_door)
                    self.agent.inventory.minus_red()

            elif self.check_collision(r_door):
                self.reward -= 1
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        for b_door in self.blue_door_list:
            "Check if self.agent has a blue key, if true then removes blue door and deducts blue total key."
            if self.agent.inventory.blue_key != 0:

                if self.check_collision(b_door):
                    self.reward += 5
                    self.game_score += 10
                    self.blue_door_list.remove(b_door)
                    self.agent.inventory.minus_blue()

            elif self.check_collision(b_door):
                self.reward -= 1
                self.agent.x = self.agent.prev_x
                self.agent.y = self.agent.prev_y

        if self.check_collision(self.flag_finish):
            GAME_WIN = True
            self.agent.game_win()
            self.game_end()

    def state(self):
        # TODO: update states that relies on object interaction
        # nearby attributes should have pixel padding between agent and object
        # on the other end box collisions will have (-) reward since we don't want our agent
        # to keep on colliding with the states. (can test w/o reward)

        # nearby constant
        NEAR_CONSTANT: float = 20.0

        a = [self.agent.x < _.x + _.width and
             self.agent.x + self.agent.width > _.x and
             self.agent.y < _.y + _.height and
             self.agent.y + self.agent.height > _.y]

        # keys in-game
        key_list = self.red_mushroom_list
        key_list.extend(self.blue_mushroom_list)

        # doors in-game
        door_list = self.red_door_list
        door_list.extend(self.blue_door_list)

        # TODO: Add try and except block if keys / doors do not exist anymore will not raise a value and make sure
        # that the state of non existing objects are `False`.

        # key referring to puzzle object key (mushrooms)
        for _key in key_list:

            # left
            if _key.x - NEAR_CONSTANT < self.agent.x:
                self.state.nearby_key = True
            # right
            if _key.x + NEAR_CONSTANT > self.agent.x:
                self.state.nearby_key = True
            # up
            if _key.y < self.agent.y - NEAR_CONSTANT:
                self.state.nearby_key = True
            # down
            if _key.y > self.agent.y + NEAR_CONSTANT:
                self.state.nearby_key = True

        for _door in door_list:

            # left
            if _door.x - NEAR_CONSTANT < self.agent.x:
                self.state.nearby_door = True
            # right
            if _door.x + NEAR_CONSTANT > self.agent.x:
                self.state.nearby_door = True
            # up
            if _door.y < self.agent.y - NEAR_CONSTANT:
                self.state.nearby_door = True
            # down
            if _door.y > self.agent.y + NEAR_CONSTANT:
                self.state.nearby_door = True

        # default_states = [self.state.up, self.state.down, self.state.right, self.state.down]
        # col_puzzle_states = [self.state.nearby_door, self.state.nearby_key, self.state.nearby_danger]
        # default_states.extend(col_puzzle_states)
        # return default_states


if __name__ == '__main__':
    game = GoblinAI(
        **GAME_SPECS.get_window_params(),
        f_screen=False,
        ai_params=AGENT_PARAMS,
        img_manager=IMAGE_MANAGER,
        puzzle_data=PUZZLE_DATA,
        stage=STAGE_A)

    pyg.clock.schedule_interval(game.update, 1 / 60.0)
    pyglet.app.run()
