import os
import re
from typing import Union

inputs_dir = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/inputs"


def load_input(day: int, strip: bool = True) -> list[str]:
    with open(f"{inputs_dir}/{day:02d}.txt", "r") as fp:
        return [line.strip() if strip else line for line in fp.readlines()]


def load_raw_input(day: int) -> str:
    with open(f"{inputs_dir}/{day:02d}.txt", "r") as fp:
        return fp.read()


def get_all_numbers_in_string(_string: str, as_strings=False) -> list[Union[int, str]]:
    return list(map(int if not as_strings else str, re.findall(r"-?\d+", _string)))


def print_solutions(part_1: int, part_2: int) -> None:
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
