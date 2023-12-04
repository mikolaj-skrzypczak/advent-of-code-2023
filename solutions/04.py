import re

from utils.utils import load_input, print_solutions

INPUT = load_input(4)


def part_1() -> int:
    score = 0
    for winning_numbers, drawn_numbers in _parse_input():
        n_wins = get_n_of_wins(winning_numbers, drawn_numbers)
        score += 2 ** (n_wins - 1) if n_wins > 0 else 0
    return score


def part_2() -> int:
    cards_owned = {i: 1 for i in range(len(INPUT))}
    for i, (winning_numbers, drawn_numbers) in enumerate(_parse_input()):
        n_wins = get_n_of_wins(winning_numbers, drawn_numbers)
        for n in range(i, i + n_wins):
            cards_owned[n + 1] += 1 * cards_owned[i]
    return sum(cards_owned.values())


def get_n_of_wins(_winning_numbers: list[int], _drawn_numbers: list[int]) -> int:
    return len(set(_winning_numbers).intersection(_drawn_numbers))


def _parse_input() -> list[tuple[list[int], list[int]]]:
    def _shrink_whitespace(_string: str) -> str:
        return re.sub(r"\s+", " ", _string)

    def _clean_numbers(_numbers: str) -> list[int]:
        return list(map(int, _shrink_whitespace(_numbers.strip()).split(" ")))

    parsed_input = []
    for line in INPUT:
        numbers = line.split(":")[1].strip()
        winning_numbers, my_numbers = numbers.split("|")
        parsed_input.append((_clean_numbers(winning_numbers), _clean_numbers(my_numbers)))

    return parsed_input


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
