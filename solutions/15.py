from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from utils.utils import print_solutions, load_raw_input

INPUT = load_raw_input(15).strip().split(",")


def part_1() -> int:
    return sum(step.hash_whole() for step in [Step(i) for i in INPUT])


def part_2() -> int:
    boxes = {i: [] for i in range(256)}
    for step in [Step(i) for i in INPUT]:
        box = step.hash_label()
        match step.operation:
            case "=":
                append_or_replace(step, boxes, box)
            case "-":
                remove_if_present(step, boxes, box)
    return calculate_focusing_power(boxes)


def append_or_replace(step: Step, boxes: dict[int, list[Step]], box: int) -> None:
    if step not in boxes[box]:
        boxes[box].append(step)
    else:
        boxes[box][boxes[box].index(step)] = step


def remove_if_present(step: Step, boxes: dict[int, list[Step]], box: int) -> None:
    if step in boxes[box]:
        boxes[box].remove(step)


def calculate_focusing_power(boxes: dict[int, list[Step]]) -> int:
    _sum = 0
    for box_num, steps in boxes.items():
        for i, step in enumerate(steps, start=1):
            _sum += (box_num + 1) * i * step.focal_length
    return _sum


@dataclass(eq=False)
class Step:
    original_string: str
    label: str
    operation: Literal["-", "="]
    focal_length: Optional[int] = None

    def __init__(self, _str: str):
        self.original_string = _str
        if "-" in _str:
            self.label = _str[:-1]
            self.operation = "-"
        else:
            self.label, focal_length = _str.split("=")
            self.focal_length = int(focal_length)
            self.operation = "="

    def hash_whole(self) -> int:
        return custom_hash(self.original_string)

    def hash_label(self) -> int:
        return custom_hash(self.label)

    def __eq__(self, other):
        return self.label == other.label


def custom_hash(_str: str) -> int:
    _hash = 0
    for char in _str:
        _hash += ord(char)
        _hash *= 17
        _hash = _hash % 256
    return _hash


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
