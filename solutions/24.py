from __future__ import annotations

import itertools
from dataclasses import dataclass
from math import floor
from typing import Optional

import numpy as np

from utils.utils import print_solutions, load_input, get_all_numbers_in_string

MIN_X_Y = 200_000_000_000_000
MAX_X_Y = 400_000_000_000_000
INPUT = load_input(24)


"""
While again part 1 was pretty straightforward and I managed to solve it with a little 
help from stackoverflow to get the intersection point of two lines, part 2 was way harder.
Honestly, I would probably never do it in a relatively acceptable time without help from the subreddit.
Kudos to @girishji for the algebraic solution to part 2.
"""

@dataclass
class Position3D:
    x: int
    y: int
    z: int


@dataclass
class Velocity3D:
    vx: int
    vy: int
    vz: int


@dataclass
class Hailstone:
    position: Position3D
    velocity: Velocity3D

    def intersection(self, other: Hailstone) -> Optional[tuple[float, float]]:
        self_x2, self_y2 = self.position.x + self.velocity.vx, self.position.y + self.velocity.vy
        other_x2, other_y2 = other.position.x + other.velocity.vx, other.position.y + other.velocity.vy
        l1 = ((self.position.x, self.position.y), (self_x2, self_y2))
        l2 = ((other.position.x, other.position.y), (other_x2, other_y2))
        intersection = line_intersection(l1, l2)
        if not intersection:
            return None
        if self.is_intersection_in_future(intersection[0]) and other.is_intersection_in_future(intersection[0]):
            return intersection

    def is_intersection_in_future(self, intersection_x: float) -> bool:
        return (intersection_x - self.position.x) / self.velocity.vx >= 0


def parse_input_to_hailstones() -> list[Hailstone]:
    return [
        Hailstone(
            Position3D(x, y, z),
            Velocity3D(vx, vy, vz)
        ) for x, y, z, vx, vy, vz in map(get_all_numbers_in_string, INPUT)
    ]


HAILSTONES = parse_input_to_hailstones()


def part_1() -> int:
    return sum(is_valid_intersection(h1, h2) for h1, h2 in itertools.combinations(HAILSTONES, 2))


def part_2() -> int:
    h1, h2, h3 = HAILSTONES[:3]
    v1 = (h1.velocity.vx, h1.velocity.vy, h1.velocity.vz)
    v2 = (h2.velocity.vx, h2.velocity.vy, h2.velocity.vz)
    v3 = (h3.velocity.vx, h3.velocity.vy, h3.velocity.vz)
    p1 = (h1.position.x, h1.position.y, h1.position.z)
    p2 = (h2.position.x, h2.position.y, h2.position.z)
    p3 = (h3.position.x, h3.position.y, h3.position.z)

    A = np.array([
        [-(v1[1] - v2[1]), v1[0] - v2[0], 0, p1[1] - p2[1], -(p1[0] - p2[0]), 0],
        [-(v1[1] - v3[1]), v1[0] - v3[0], 0, p1[1] - p3[1], -(p1[0] - p3[0]), 0],

        [0, -(v1[2] - v2[2]), v1[1] - v2[1], 0, p1[2] - p2[2], -(p1[1] - p2[1])],
        [0, -(v1[2] - v3[2]), v1[1] - v3[1], 0, p1[2] - p3[2], -(p1[1] - p3[1])],

        [-(v1[2] - v2[2]), 0, v1[0] - v2[0], p1[2] - p2[2], 0, -(p1[0] - p2[0])],
        [-(v1[2] - v3[2]), 0, v1[0] - v3[0], p1[2] - p3[2], 0, -(p1[0] - p3[0])]
    ])

    b = [
        (p1[1] * v1[0] - p2[1] * v2[0]) - (p1[0] * v1[1] - p2[0] * v2[1]),
        (p1[1] * v1[0] - p3[1] * v3[0]) - (p1[0] * v1[1] - p3[0] * v3[1]),

        (p1[2] * v1[1] - p2[2] * v2[1]) - (p1[1] * v1[2] - p2[1] * v2[2]),
        (p1[2] * v1[1] - p3[2] * v3[1]) - (p1[1] * v1[2] - p3[1] * v3[2]),

        (p1[2] * v1[0] - p2[2] * v2[0]) - (p1[0] * v1[2] - p2[0] * v2[2]),
        (p1[2] * v1[0] - p3[2] * v3[0]) - (p1[0] * v1[2] - p3[0] * v3[2])
    ]

    return floor(sum(np.linalg.solve(A, b)[:3]))


def is_valid_intersection(hailstone_1: Hailstone, hailstone_2: Hailstone) -> bool:
    if intersection := hailstone_1.intersection(hailstone_2):
        if MIN_X_Y <= intersection[0] <= MAX_X_Y and MIN_X_Y <= intersection[1] <= MAX_X_Y:
            return True
    return False


# https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def line_intersection(
        line1: tuple[tuple[int, int], tuple[int, int]],
        line2: tuple[tuple[int, int], tuple[int, int]]
) -> Optional[tuple[float, float]]:
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
