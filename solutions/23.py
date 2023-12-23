import re
from collections import deque, defaultdict
from math import inf
from typing import NamedTuple, Generator

from utils.utils import load_input, print_solutions

GRID = load_input(23)
GRID_HEIGHT = len(GRID)
GRID_WIDTH = len(GRID[0])
FOREST = "#"
PATH = "."
RIGHT_SLOPE = ">"
LEFT_SLOPE = "<"
DOWN_SLOPE = "v"
intersection_connection = NamedTuple("IntersectionConnection", [("to", tuple[int, int]), ("length", int)])

"""
The optimization idea for part 2 was taken from the subreddit. Many people from the community discussed an
option to DFS through intersections only. This idea came out to be good enough to solve part 2 in reasonable time,
as an approach from part 1 couldn't find solution in several hours (and the queue size rose to more than 250k items).
"""


class Directions:
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


DIRECTIONS = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]


def part_1(start: tuple[int, int], target: tuple[int, int]) -> int:
    return find_longest_path(start, target, part=1)


def part_2(start: tuple[int, int], target: tuple[int, int]) -> int:
    return find_longest_path(start, target, part=2)


def find_longest_path(start: tuple[int, int], target: tuple[int, int], part: int) -> int:
    match part:
        case 1:
            return get_longest_path_naive_dfs(start, target)
        case 2:
            replace_slopes_with_path()
            return find_longest_path_dfs_through_intersections(start, target)


def get_longest_path_naive_dfs(start: tuple[int, int], target: tuple[int, int]) -> int:
    longest_path_len = -inf
    dq = deque([[start]])
    while dq:
        path = dq.popleft()
        if path[-1] == target:
            longest_path_len = max(longest_path_len, len(path) - 1)
            continue
        for new_path in get_new_paths_naive_dfs(path):
            dq.append(new_path)
    return longest_path_len


def get_new_paths_naive_dfs(path: list[tuple[int, int]]) -> Generator[list[tuple[int, int]]]:
    previous_position = path[-1]
    for direction in DIRECTIONS:
        new_position = (previous_position[0] + direction[0], previous_position[1] + direction[1])
        if new_position in path:
            continue
        if is_object_at_position(new_position, PATH):
            yield path + [new_position]
        elif is_object_at_position(new_position, RIGHT_SLOPE) and direction == Directions.RIGHT:
            yield path + [new_position, (new_position[0], new_position[1] + 1)]
        elif is_object_at_position(new_position, LEFT_SLOPE) and direction == Directions.LEFT:
            yield path + [new_position, (new_position[0], new_position[1] - 1)]
        elif is_object_at_position(new_position, DOWN_SLOPE) and direction == Directions.DOWN:
            yield path + [new_position, (new_position[0] + 1, new_position[1])]


def find_longest_path_dfs_through_intersections(start: tuple[int, int], target: tuple[int, int]) -> int:
    intersections_connections = get_all_intersections_direct_connections(
        get_all_intersections().union({start, target})
    )
    return _find__longest_path_dfs_through_intersections(start, target, intersections_connections)


def _find__longest_path_dfs_through_intersections(
        start: tuple[int, int],
        target: tuple[int, int],
        intersections_connections: dict[tuple[int, int], set[intersection_connection]]
) -> int:
    dq = deque([(start, [], 0)])
    max_path_len = 0
    while dq:
        current_intersection, path, path_len = dq.pop()
        if current_intersection == target:
            max_path_len = max(max_path_len, path_len)
            continue
        for connected_intersection, connection_length in intersections_connections[current_intersection]:
            if connected_intersection not in path:
                dq.append((
                    connected_intersection,
                    path + [current_intersection],
                    path_len + connection_length
                ))
    return max_path_len


def get_all_intersections_direct_connections(
        intersections: set[tuple[int, int]]
) -> dict[tuple[int, int], set[intersection_connection]]:
    intersections_connections = defaultdict(set)
    for intersection in intersections:
        dq = deque([(intersection, set())])
        while dq:
            position, visited = dq.popleft()
            if position in visited:
                continue
            visited.add(position)
            for direction in DIRECTIONS:
                new_position = (position[0] + direction[0], position[1] + direction[1])
                if (
                        is_within_bounds(new_position) and
                        is_object_at_position(position, PATH) and
                        new_position not in visited
                ):
                    if new_position in intersections:
                        intersections_connections[intersection].add(intersection_connection(new_position, len(visited)))
                        intersections_connections[new_position].add(intersection_connection(intersection, len(visited)))
                    else:
                        dq.append((new_position, visited.union({position})))
    return intersections_connections


def get_all_intersections() -> set[tuple[int, int]]:
    intersections = set()
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if is_object_at_position((y, x), PATH) and is_intersection((y, x)):
                intersections.add((y, x))
    return intersections


def is_object_at_position(position: tuple[int, int], _object: str) -> bool:
    return GRID[position[0]][position[1]] == _object


def get_starting_position() -> tuple[int, int]:
    return 0, GRID[0].index(PATH)


def get_target_position() -> tuple[int, int]:
    return len(GRID) - 1, GRID[-1].index(PATH)


def replace_slopes_with_path() -> None:
    global GRID
    GRID = [re.sub(rf"[{''.join([RIGHT_SLOPE, LEFT_SLOPE, DOWN_SLOPE])}]", PATH, line) for line in GRID]


def main() -> None:
    start = get_starting_position()
    target = get_target_position()
    print_solutions(part_1(start, target), part_2(start, target))


def is_intersection(position: tuple[int, int]) -> bool:
    return sum(
        1 for direction in DIRECTIONS
        if is_object_at_position((position[0] + direction[0], position[1] + direction[1]), PATH)
    ) > 2


def is_within_bounds(position: tuple[int, int]) -> bool:
    return 0 <= position[0] < GRID_HEIGHT and 0 <= position[1] < GRID_WIDTH


if __name__ == '__main__':
    main()
