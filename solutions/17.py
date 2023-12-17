from collections import defaultdict
from heapq import heappush, heappop
from math import inf
from typing import NamedTuple, Optional

from utils.utils import load_input, print_solutions

GRID = load_input(17)
Position = NamedTuple("Position", [("y", int), ("x", int)])
State = NamedTuple("State", [("position", Position), ("direction", tuple[int, int])])
Item = NamedTuple("Item", [("cost", int), ("state", State)])
TARGET = Position(len(GRID) - 1, len(GRID[0]) - 1)


def part_1() -> int:
    return find_shortest_path(shortest_move=1, longest_move=3)


def part_2() -> int:
    return find_shortest_path(shortest_move=4, longest_move=10)


def find_shortest_path(shortest_move: int, longest_move: int) -> Optional[int]:
    def move_forward(_new_cost: int):
        for steps in range(1, longest_move + 1):
            new_position = Position(
                y=current_state.position.y + new_direction[0] * steps,
                x=current_state.position.x + new_direction[1] * steps
            )
            if not is_in_grid_bounds(new_position):
                continue
            _new_cost += int(GRID[new_position.y][new_position.x])
            if steps < shortest_move:
                continue
            new_state = State(new_position, new_direction)
            if _new_cost < costs[new_state]:
                costs[new_state] = _new_cost
                heappush(heap, (_new_cost, new_state))

    costs = defaultdict(lambda: inf)
    heap = initialize_heap()
    while heap:
        current_cost, current_state = heappop(heap)
        if current_state.position == TARGET:
            return current_cost
        if current_cost > costs[current_state]:
            continue
        for new_direction in turn_both_sides(current_state.direction):
            new_cost = current_cost
            move_forward(new_cost)


def initialize_heap() -> list[Item]:
    return [
        Item(cost=0, state=State(position=Position(y=0, x=0), direction=(0, 1))),
        Item(cost=0, state=State(position=Position(y=0, x=0), direction=(1, 0))),
    ]


def turn_both_sides(previous_direction: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (-previous_direction[1], previous_direction[0]), (previous_direction[1], -previous_direction[0])


def is_in_grid_bounds(position: Position) -> bool:
    return 0 <= position.y <= TARGET.y and 0 <= position.x <= TARGET.x


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
