from collections import deque
from math import ceil
from typing import NamedTuple, Callable

from utils.utils import print_solutions, load_input

GRID = load_input(21)
GRID_WIDTH, GRID_HEIGHT = len(GRID[0]), len(GRID)
Position = NamedTuple("Position", [("y", int), ("x", int)])

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
ROCK = "#"

"""
While I easily solved part 1 on my own. To solve part 2 I had to look at the subreddit.
Kudos to @mebeim for the algorithm used in part2, but even they stated that:

"could not figure it out by myself, checked the megathread for useful comments" - power of the community! :)

PS: The logic of get_n_of_reachable_squares function could be changed to make it a lot faster, 
but as I implemented it completely on my own, I'm happy with it staying here.
"""


def part_1() -> int:
    return get_n_of_reachable_squares(available_steps=64, get_new_positions_fn=get_new_positions_p1)


def part_2() -> int:
    steps = 26501365
    mod = 26501365 % GRID_HEIGHT

    first = get_n_of_reachable_squares(available_steps=mod, get_new_positions_fn=get_new_positions_p2)
    second = get_n_of_reachable_squares(available_steps=mod + GRID_HEIGHT, get_new_positions_fn=get_new_positions_p2)
    third = get_n_of_reachable_squares(available_steps=mod + GRID_HEIGHT * 2, get_new_positions_fn=get_new_positions_p2)

    first_diff1 = second - first
    first_diff2 = third - second
    second_diff = first_diff2 - first_diff1

    # https://www.radfordmathematics.com/algebra/sequences-series/difference-method-sequences/quadratic-sequences.html
    a = second_diff // 2
    b = first_diff1 - 3 * a
    c = first - b - a

    def calculate_answer(n: int) -> int:
        return a * n ** 2 + b * n + c

    return calculate_answer(ceil(steps / GRID_HEIGHT))


def get_n_of_reachable_squares(
        available_steps: int,
        get_new_positions_fn: Callable[[Position], list[Position]]
) -> int:
    dq = deque([(get_starting_position(), available_steps)])
    reached_positions = set()
    states_visited = set()
    while dq:
        position, steps = dq.popleft()
        if (position, steps) in states_visited:
            continue
        states_visited.add((position, steps))
        if steps == 0:
            reached_positions.add(position)
            continue
        for new_position in get_new_positions_fn(position):
            dq.append((new_position, steps - 1))
    return len(reached_positions)


def get_new_positions_p1(position: Position) -> list[Position]:
    positions = []
    for direction in (UP, RIGHT, DOWN, LEFT):
        new_position = Position(position.y + direction[0], position.x + direction[1])
        if is_valid_position(new_position):
            positions.append(new_position)
    return positions


def get_new_positions_p2(position: Position) -> list[Position]:
    positions = []
    for direction in (UP, RIGHT, DOWN, LEFT):
        new_position = Position(position.y + direction[0], position.x + direction[1])
        if GRID[new_position.y % GRID_HEIGHT][new_position.x % GRID_WIDTH] != ROCK:
            positions.append(new_position)
    return positions


def get_starting_position() -> Position:
    for y, row in enumerate(GRID):
        for x, char in enumerate(row):
            if char == "S":
                return Position(y, x)


def is_valid_position(position: Position) -> bool:
    return not is_out_of_grid(position) and GRID[position.y][position.x] != ROCK


def is_out_of_grid(position: Position) -> bool:
    return position.y < 0 or position.y >= len(GRID) or position.x < 0 or position.x >= len(GRID[0])


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
