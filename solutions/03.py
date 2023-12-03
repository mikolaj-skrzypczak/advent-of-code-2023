import re
from collections import defaultdict

from utils.utils import load_input, print_solutions

INPUT = load_input(3)


def part_1() -> int:
    number_pattern = re.compile(r"\d+")
    _sum = 0
    for i, line in enumerate(INPUT):
        for match in re.finditer(number_pattern, line):
            j = match.start()
            while j < match.end():
                if has_symbol_in_any_surrounding_field(i, j):
                    _sum += int(match.group())
                    break
                j += 1
    return _sum


def part_2() -> int:
    number_pattern = re.compile(r"\d+")
    gears = defaultdict(list)

    for i, line in enumerate(INPUT):
        for match in re.finditer(number_pattern, line):
            j = match.start()
            close_gears = []
            while j < match.end():
                close_gears.extend(get_gears_from_surrounding_fields(i, j))
                j += 1
            close_gears = list(set(close_gears))
            for gear in close_gears:
                gears[gear].append(int(match.group()))

    _sum = 0
    for v in gears.values():
        if len(v) == 2:
            _sum += v[0] * v[1]

    return _sum


def has_symbol_in_any_surrounding_field(i: int, j: int):
    for _i in range(i - 1, i + 2):
        for _j in range(j - 1, j + 2):
            if _i == i and _j == j:
                continue
            if _i < 0 or _j < 0 or _i >= len(INPUT) or _j >= len(INPUT[0]):
                continue
            if INPUT[_i][_j] != "." and not INPUT[_i][_j].isdigit():
                return True
    return False


def get_gears_from_surrounding_fields(i: int, j: int) -> list[tuple]:
    gears = []
    for _i in range(i - 1, i + 2):
        for _j in range(j - 1, j + 2):
            if _i == i and _j == j:
                continue
            if _i < 0 or _j < 0 or _i >= len(INPUT) or _j >= len(INPUT[0]):
                continue
            if INPUT[_i][_j] == "*":
                gears.append((_i, _j))
    return gears


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
