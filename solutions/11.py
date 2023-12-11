from utils.utils import print_solutions, load_input
from itertools import combinations
from typing import NamedTuple

GRID = list(map(list, load_input(11)))

Galaxy = NamedTuple("Galaxy", [("y", int), ("x", int)])


def part_1(all_galaxies_pairs: list[tuple[Galaxy, Galaxy]]) -> int:
    return solve(all_galaxies_pairs, expanded_by=2)


def part_2(all_galaxies_pairs: list[tuple[Galaxy, Galaxy]]) -> int:
    return solve(all_galaxies_pairs, expanded_by=1_000_000)


def solve(all_galaxies_pairs: list[tuple[Galaxy, Galaxy]], expanded_by: int) -> int:
    return sum(calculate_2d_plane_distance(*pair, expanded_by=expanded_by) for pair in all_galaxies_pairs)


def calculate_2d_plane_distance(galaxy_1: Galaxy, galaxy_2: Galaxy, expanded_by: int) -> int:
    def account_for_world_expansion(_initial_distance: int) -> int:
        return account_for_rows_expansion(account_for_cols_expansion(_initial_distance))

    def account_for_rows_expansion(_distance: int) -> int:
        for col in range(*(galaxy_1.x, galaxy_2.x) if galaxy_1.x < galaxy_2.x else (galaxy_2.x, galaxy_1.x)):
            if all(row[col] == "." for row in GRID):
                _distance += expanded_by - 1
        return _distance

    def account_for_cols_expansion(_distance: int) -> int:
        for row in range(*(galaxy_1.y, galaxy_2.y) if galaxy_1.y < galaxy_2.y else (galaxy_2.y, galaxy_1.y)):
            if all(char == "." for char in GRID[row]):
                _distance += expanded_by - 1
        return _distance

    initial_distance = abs(galaxy_1.y - galaxy_2.y) + abs(galaxy_1.x - galaxy_2.x)
    distance = account_for_world_expansion(initial_distance)

    return distance


def get_all_galaxies() -> list[tuple[int, int]]:
    galaxies = []
    for y in range(len(GRID)):
        for x in range(len(GRID[0])):
            if GRID[y][x] == "#":
                galaxies.append(Galaxy(y, x))
    return galaxies


def get_all_galaxies_pairs(galaxies: list[Galaxy]) -> list[tuple[Galaxy, Galaxy]]:
    return list(combinations(galaxies, 2))


def main():
    galaxies_pairs = get_all_galaxies_pairs(get_all_galaxies())
    print_solutions(part_1(galaxies_pairs), part_2(galaxies_pairs))


if __name__ == '__main__':
    main()
