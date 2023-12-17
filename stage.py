import json
import time
from pathlib import Path
from typing import Callable

import inquirer
import pandas as pd

PIXEL_FACTOR = 32


def transform_col_by_code(col: str, c: str, raw_map: pd.DataFrame) -> list[tuple]:
    to_tuple: Callable = lambda x: (x, int(col))
    code_index = raw_map[raw_map.loc[:, col] == c][col].index
    code_list = list(code_index)
    tuple_code_list = [to_tuple(x) for x in code_list]

    return tuple_code_list


def multiply_by_pixel(transformed_code_list: list[tuple], px_factor: int) \
        -> list[tuple]:
    return [(x * px_factor, y * px_factor) for y, x in transformed_code_list]


def make_map(_map: pd.DataFrame):
    puzzle_objects = {
        'ai': [],
        'fg': [],
        'b': [],
        'sp': [],
        'bs': [],
        'rs': [],
        'rd': [],
        'bd': [],
    }

    map_cols = _map.columns
    _cols = list(map_cols)
    _c = [k for k in puzzle_objects.keys()]

    for c in _c:
        for cols in _cols:
            t = transform_col_by_code(cols, c, _map)
            m = multiply_by_pixel(t, PIXEL_FACTOR)
            for x, y in m:
                puzzle_objects.get(c).append((x, y))

    return puzzle_objects


if __name__ == '__main__':
    maps_dir = Path.cwd() / 'maps'
    a = [x.name for x in maps_dir.iterdir() if x.name.endswith('.csv')]

    questions = [
        inquirer.List('choice',
                      message="What size do you need?",
                      choices=a,
                      ),
    ]
    answers = inquirer.prompt(questions)
    load_choice = [x for x in maps_dir.iterdir() if x.name == answers.get('choice')]
    loaded_map = pd.read_csv(load_choice[0])
    loaded_map = loaded_map.set_index(loaded_map.columns[0])
    json_file = make_map(loaded_map)
    save_name = str.rstrip(answers.get('choice'), '.csv') + '.json'

    with open(maps_dir / save_name, 'w') as f:
        json.dump(json_file, f)

    print(f"CSV map converted to json with name {save_name}")
    time.sleep(.5)
