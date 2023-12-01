from util.common_imports import *
from stage import WallGenerator
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

background_path = Path.cwd() / "assets" / "background" / "game_bg.png"
background_image = pyg.image.load(background_path)

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

""" Wall & Stage """
wall_filepath = Path.cwd() / "assets" / "sprite" / "wall" / "crate.png"
wall_image = pyg.image.load(wall_filepath)

box_batch = pyg.graphics.Batch()
box_sprites = []
wall = WallGenerator(wall_image, WINDOW_HEIGHT, WINDOW_WIDTH, batch=box_batch)
