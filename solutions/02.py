import re
from collections import defaultdict

from utils.utils import load_input, print_solutions

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

INPUT = load_input(2)
GAME_ID_PATTERN = r"(\d+):"
DRAWS_PATTERN = r"(\d+ \w+)"


def part_1() -> int:
    def _are_valid(_draws: list) -> bool:
        for draw in _draws:
            n_drawn, color = draw.split(" ")
            if int(n_drawn) > LIMITS[color]:
                return False
        return True

    _input = parse_input()
    valid_ids_sum = 0
    for game_id, draws in _input:
        if _are_valid(draws):
            valid_ids_sum += int(game_id)
    return valid_ids_sum


def part_2() -> int:
    def _get_local_minima(_draws: list) -> dict:
        _local_minima = defaultdict(int)
        for draw in _draws:
            n_drawn, color = draw.split(" ")
            _local_minima[color] = max(_local_minima[color], int(n_drawn))
        return _local_minima

    def _calculate_power(_local_minima: dict) -> int:
        _power = 1
        for _, v in _local_minima.items():
            _power *= v
        return _power

    _input_ = parse_input()
    powers = 0
    for game_id, draws in _input_:
        local_minima = _get_local_minima(draws)
        powers += _calculate_power(local_minima)
    return powers


def parse_input() -> list[tuple[int, list]]:
    games = []
    for game in INPUT:
        game_id = re.search(GAME_ID_PATTERN, game).group(1)
        draws = re.findall(DRAWS_PATTERN, game)
        games.append((int(game_id), draws))
    return games


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
