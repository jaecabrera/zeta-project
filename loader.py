import configparser
import json
from pathlib import Path
import pyglet as pyg

from util.images import ImageManager
from util.specs import GameSpecs

with open('./maps/stage_a.json', 'r') as f:
    STAGE_A = json.load(f)

# Config
config = configparser.ConfigParser()
config.read('config.ini')
relative_image_fp = {k: config['PATHS'][v] for k, v in zip(config['PATHS'], config['PATHS'])}

# Game and Image Managers
IMAGE_MANAGER = ImageManager(relative_image_fp)
GAME_SPECS = GameSpecs()
IMAGE_MANAGER.load_pyglet_images()

agent_img_fp = Path.cwd() / "assets" / "sprite" / "bot" / "bot.gif"
animation = pyg.image.load_animation(agent_img_fp)
sprite = pyg.sprite.Sprite(animation)

AGENT_PARAMS = {
    'sprite_grid': animation,
    'x': 64,
    'y': 64,
    'spd': 30,
}
