from dataclasses import dataclass


@dataclass(slots=True)
class GameSpecs:
    win_width = 1024
    win_height = 768
    speed = 120

    def get_window_params(self) -> dict:
        return dict(width=self.win_width, height=self.win_height)
