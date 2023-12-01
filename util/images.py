from dataclasses import field

from common_imports import *


@dataclass(slots=True, init=False)
class ImageManager:
    image_environment: dict[str, str] = field(default_factory=dict)
    image_relative_path: dict[str, Path] = field(init=False, default=None)
    pyglet_images: dict[str, pyg.image] = field(init=False, default=None)

    def __init__(self, image_env: dict[str, str]):
        self.image_environment = image_env
        self.load_rel_path()

    def load_rel_path(self):
        self.image_relative_path = {k: Path.cwd() / 'sprite' / v for k, v in self.image_environment.items()}

    def load_pyglet_images(self):
        self.pyglet_images = {k: pyg.image.load(v) for k, v in self.image_relative_path.items()}
