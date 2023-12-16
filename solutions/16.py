from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from queue import Queue
from typing import NamedTuple

from utils.utils import print_solutions, load_input

GRID = load_input(16)


def part_1() -> int:
    starting_beam = Beam(Position(-1, 0), Directions.RIGHT)
    return energize_grid(starting_beam)


def part_2() -> int:
    max_energize = 0
    starting_beams = [
        *[Beam(Position(-1, x), Directions.RIGHT) for x in range(len(GRID))],
        *[Beam(Position(y, -1), Directions.DOWN) for y in range(len(GRID[0]))],
        *[Beam(Position(len(GRID), x), Directions.LEFT) for x in range(len(GRID))],
        *[Beam(Position(y, len(GRID[0])), Directions.UP) for y in range(len(GRID[0]))]
    ]
    for starting_beam in starting_beams:
        max_energize = max(max_energize, energize_grid(starting_beam))
    return max_energize


def energize_grid(starting_beam: Beam):
    q = Queue()
    q.put(starting_beam)
    energized = defaultdict(set)
    beam_move_handler = BeamMoveHandler()
    while not q.empty():
        beam = q.get()
        next_position = beam.get_next_position()
        if is_out_of_bounds(next_position) or already_checked(energized, beam.direction, next_position):
            continue

        energized[next_position].add(beam.direction)
        beam_move_handler.handle(GRID[next_position.x][next_position.y], beam, next_position, q)

    return len(energized)


def is_out_of_bounds(position: Position) -> bool:
    return position.y < 0 or position.x < 0 or position.y >= len(GRID) or position.x >= len(GRID[0])


def already_checked(energized: dict[Position, set[Direction]], direction: Direction, position: Position) -> bool:
    return position in energized and direction in energized[position]


Position = NamedTuple("Position", [("y", int), ("x", int)])
Direction = NamedTuple("Direction", [("y", int), ("x", int)])


class Directions:
    UP = Direction(0, -1)
    DOWN = Direction(0, 1)
    LEFT = Direction(-1, 0)
    RIGHT = Direction(1, 0)


@dataclass
class Beam:
    position: Position
    direction: Direction

    def get_next_position(self) -> Position:
        return Position(self.position.y + self.direction.y, self.position.x + self.direction.x)


class BeamMoveHandler:
    BACKSLASH_OLD_TO_NEW_DIRECTION = {
        Directions.RIGHT: Directions.DOWN,
        Directions.LEFT: Directions.UP,
        Directions.UP: Directions.LEFT,
        Directions.DOWN: Directions.RIGHT
    }

    SLASH_OLD_TO_NEW_DIRECTION = {
        Directions.RIGHT: Directions.UP,
        Directions.LEFT: Directions.DOWN,
        Directions.UP: Directions.RIGHT,
        Directions.DOWN: Directions.LEFT
    }

    def __init__(self):
        self.tile_type_to_function = {
            ".": self._handle_dot,
            "-": self._handle_horizontal,
            "|": self._handle_vertical,
            "/": self._handle_slash,
            "\\": self._handle_backslash
        }

    def handle(self, tile: str, beam: Beam, next_position: Position, q: Queue) -> None:
        self.tile_type_to_function[tile](beam, next_position, q)

    @staticmethod
    def _handle_dot(beam: Beam, next_position, q: Queue) -> None:
        q.put(Beam(next_position, beam.direction))

    @staticmethod
    def _handle_horizontal(beam: Beam, next_position, q: Queue) -> None:
        if beam.direction == Directions.RIGHT or beam.direction == Directions.LEFT:
            q.put(Beam(next_position, beam.direction))
        else:
            q.put(Beam(next_position, Directions.RIGHT))
            q.put(Beam(next_position, Directions.LEFT))

    @staticmethod
    def _handle_vertical(beam: Beam, next_position, q: Queue) -> None:
        if beam.direction == Directions.UP or beam.direction == Directions.DOWN:
            q.put(Beam(next_position, beam.direction))
        else:
            q.put(Beam(next_position, Directions.UP))
            q.put(Beam(next_position, Directions.DOWN))

    @classmethod
    def _handle_slash(cls, beam: Beam, next_position, q: Queue) -> None:
        q.put(Beam(next_position, cls.SLASH_OLD_TO_NEW_DIRECTION[beam.direction]))

    @classmethod
    def _handle_backslash(cls, beam: Beam, next_position, q: Queue) -> None:
        q.put(Beam(next_position, cls.BACKSLASH_OLD_TO_NEW_DIRECTION[beam.direction]))


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
