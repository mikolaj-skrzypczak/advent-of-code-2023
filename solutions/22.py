from collections import deque
from dataclasses import dataclass

from utils.utils import load_input, get_all_numbers_in_string, print_solutions

INPUT = load_input(22)


@dataclass
class Position3D:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    id: int
    start: Position3D
    end: Position3D


def parse_input_to_bricks() -> dict[int, Brick]:
    bricks = {}
    for ind, (x1, y1, z1, x2, y2, z2) in enumerate(
            sorted(list(map(get_all_numbers_in_string, INPUT)), key=lambda x: (min(x[2], x[5]), max(x[2], x[5])))):
        bricks[ind] = Brick(
            ind,
            Position3D(min(x1, x2), min(y1, y2), min(z1, z2)),
            Position3D(max(x1, x2), max(y1, y2), max(z1, z2))
        )
    return bricks


BRICK_ID = int
SPOT_TO_OCCUPIED_BY_BRICK: dict[tuple[int, int, int], BRICK_ID] = {}
BRICKS = parse_input_to_bricks()


def main() -> None:
    let_bricks_fall()
    print_solutions(part_1(), part_2())


def part_1() -> int:
    return sum(1 if can_be_disintegrated(brick) else 0 for brick in BRICKS.values())


def part_2() -> int:
    return sum(get_n_brick_that_would_fall_if_disintegrated(brick) for brick in BRICKS.values())


def let_bricks_fall() -> None:
    for _id, brick in BRICKS.items():

        while not get_bricks_touching_bottom(brick) and brick.start.z > 1:
            brick.start.z -= 1
            brick.end.z -= 1

        for x in range(brick.start.x, brick.end.x + 1):
            for y in range(brick.start.y, brick.end.y + 1):
                for z in range(brick.start.z, brick.end.z + 1):
                    SPOT_TO_OCCUPIED_BY_BRICK[(x, y, z)] = brick.id


def can_be_disintegrated(brick: Brick) -> bool:
    touching_above = get_bricks_touching_top(brick)
    if not touching_above:
        return True
    for brick_id in touching_above:
        bricks_below_the_one_above = get_bricks_touching_bottom(BRICKS[brick_id])
        if len(bricks_below_the_one_above) == 1:
            break
    else:
        return True


def get_n_brick_that_would_fall_if_disintegrated(brick: Brick) -> int:
    dq = deque([brick])
    supporting_bricks = {brick.id}
    while dq:
        brick = dq.pop()
        touching_above = get_bricks_touching_top(brick)
        for brick_id in touching_above:
            touching_below = get_bricks_touching_bottom(BRICKS[brick_id])
            if len(touching_below - supporting_bricks) == 0:
                supporting_bricks.add(brick_id)
                dq.append(BRICKS[brick_id])
    return len(supporting_bricks) - 1


def get_bricks_touching_bottom(brick: Brick) -> set[BRICK_ID]:
    touching = set()
    z = brick.start.z - 1
    if z == 0:
        return touching
    iterate_through_x_and_y_and_call(brick, z, add_to_touching_if_occupied, touching)
    return touching


def get_bricks_touching_top(brick: Brick) -> set[BRICK_ID]:
    touching = set()
    z = brick.end.z + 1
    iterate_through_x_and_y_and_call(brick, z, add_to_touching_if_occupied, touching)
    return touching


def iterate_through_x_and_y_and_call(brick: Brick, z: int, fn: callable, touching: set) -> None:
    for x in range(brick.start.x, brick.end.x + 1):
        for y in range(brick.start.y, brick.end.y + 1):
            fn(x, y, z, touching)


def add_to_touching_if_occupied(x: int, y: int, z: int, touching: set[BRICK_ID]) -> None:
    if (x, y, z) in SPOT_TO_OCCUPIED_BY_BRICK:
        touching.add(SPOT_TO_OCCUPIED_BY_BRICK[(x, y, z)])


if __name__ == '__main__':
    main()
