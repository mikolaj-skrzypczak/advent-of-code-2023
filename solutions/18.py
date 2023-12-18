from typing import NamedTuple, Callable

import numpy as np

from utils.utils import print_solutions, load_input

INPUT = load_input(18)

DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
    "0": (0, 1),
    "1": (1, 0),
    "2": (0, -1),
    "3": (-1, 0)
}

Vertex = NamedTuple("Vertex", [("row", int), ("col", int)])
parse_instructions_fn_type = Callable[[str], tuple[tuple[int, int], int, str]]


def part_1() -> int:
    return solve(parse_original_instructions)


def part_2() -> int:
    return solve(parse_modified_instructions)


def solve(parse_instructions_func: parse_instructions_fn_type) -> int:
    vertices = get_polygon_vertices(parse_instructions_func)
    area = polygon_area(
        xs=np.array([p[0] for p in vertices]),
        ys=np.array([p[1] for p in vertices])
    )
    circumference = polygon_circumference(vertices)
    return int((area + 1 - circumference // 2) + circumference)


def get_polygon_vertices(parse_instructions_func: parse_instructions_fn_type) -> list[Vertex]:
    current_vertex = Vertex(0, 0)
    path = [current_vertex]
    for instruction in INPUT:
        previous_point = current_vertex
        direction, steps, _ = parse_instructions_func(instruction)
        current_vertex = Vertex(
            row=previous_point.row + direction[0] * steps,
            col=previous_point.col + direction[1] * steps
        )
        path.append(current_vertex)
    return path


def parse_original_instructions(line: str) -> tuple[tuple[int, int], int, str]:
    direction, steps, color = line.split()
    return DIRECTIONS[direction], int(steps), color


def parse_modified_instructions(line: str) -> tuple[tuple[int, int], int, str]:
    _, _, color = line.split()
    color = color[2:-1]
    return DIRECTIONS[color[-1]], hex_to_dec(color[:-1]), color


def hex_to_dec(_hex: str) -> int:
    return int(_hex, 16)


def polygon_area(xs: np.ndarray, ys: np.ndarray) -> float:
    return 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))


def polygon_circumference(path: list[Vertex]) -> int:
    return sum(distance(path[i], path[i + 1]) for i in range(len(path) - 1))


def distance(v1: Vertex, v2: Vertex) -> int:
    return abs(v1.row - v2.row) + abs(v1.col - v2.col)


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == "__main__":
    main()
