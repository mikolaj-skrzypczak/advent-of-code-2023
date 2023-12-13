from typing import Callable, Union

from Levenshtein import distance

from utils.utils import print_solutions, load_raw_input

INPUT = [i.split("\n") for i in load_raw_input(13).split("\n\n")]


def part_1() -> int:
    return solve(
        vertical_scoring_algorith=get_vertical_reflection,
        horizontal_scoring_algorith=get_horizontal_reflection
    )


def part_2() -> int:
    return solve(
        vertical_scoring_algorith=get_vertical_reflection_with_one_wrong_tile,
        horizontal_scoring_algorith=get_horizontal_reflection_with_one_wrong_tile
    )


def solve(
        vertical_scoring_algorith: Callable[[list[str]], int],
        horizontal_scoring_algorith: Callable[[list[str]], int]
) -> int:
    return sum(get_grid_score(grid, vertical_scoring_algorith, horizontal_scoring_algorith) for grid in INPUT)


def get_grid_score(
        grid: list[str],
        vertical_scoring_algorith: Callable[[list[str]], int],
        horizontal_scoring_algorith: Callable[[list[str]], int]
) -> int:
    if cols_to_left := vertical_scoring_algorith(grid):
        return cols_to_left
    if rows_above := horizontal_scoring_algorith(grid):
        return 100 * rows_above


def get_vertical_reflection(grid: list[str]) -> Union[int, None]:
    for y in range(1, len(grid[0])):
        dist_to_border = min(y, len(grid[0]) - y)
        if all(grid[i][y - dist_to_border:y] == (grid[i][y:y + dist_to_border][::-1]) for i in range(len(grid))):
            return y


def get_horizontal_reflection(grid: list[str]) -> Union[int, None]:
    for x in range(1, len(grid)):
        dist_to_border = min(x, len(grid) - x)
        if grid[x - dist_to_border:x] == grid[x:x + dist_to_border][::-1]:
            return x


def get_horizontal_reflection_with_one_wrong_tile(grid: list[str]) -> Union[int, None]:
    for x in range(1, len(grid)):
        dist_to_border = min(x, len(grid) - x)
        top = grid[x - dist_to_border:x]
        bottom = grid[x:x + dist_to_border][::-1]
        if could_be_reflection(top, bottom):
            return x


def get_vertical_reflection_with_one_wrong_tile(grid: list[str]) -> Union[int, None]:
    for y in range(1, len(grid[0])):
        dist_to_border = min(y, len(grid[0]) - y)
        left = [i[y - dist_to_border:y] for i in grid]
        right = [i[y:y + dist_to_border][::-1] for i in grid]
        if could_be_reflection(left, right):
            return y


def could_be_reflection(first: list[str], second: list[str]) -> bool:
    differ_by_one_tile = [differ_by_one_char(i, j) for i, j in zip(first, second)]
    are_equal = [i == j for i, j in zip(first, second)]
    return differ_by_one_tile.count(True) == 1 and are_equal.count(True) == len(are_equal) - 1


def differ_by_one_char(s1: str, s2: str) -> bool:
    return distance(s1, s2) == 1


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
