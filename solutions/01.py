import re

import inflect

from utils.utils import load_input, print_solutions

INPUT = load_input(1)
IE = inflect.engine()


def part_1() -> int:
    regexp = r"(\d)"
    control_digits = []
    for line in INPUT:
        numbers = re.findall(regexp, line)
        control_digit = f"{numbers[0]}{numbers[-1]}"
        control_digits.append(int(control_digit))

    return sum(control_digits)


def part_2() -> int:
    def _get_control_digit(_line: str):
        all_occurrences_with_indexes = set()
        for k, v in regexps_to_values.items():
            if k in _line:
                all_occurrences_with_indexes.add((_line.find(k), v))
                all_occurrences_with_indexes.add((_line.rfind(k), v))
        _sorted_by_occurrence_ind = sorted(list(all_occurrences_with_indexes), key=lambda x: x[0])
        return int(f"{_sorted_by_occurrence_ind[0][1]}{_sorted_by_occurrence_ind[-1][1]}")

    regexps_to_values = {
        **{IE.number_to_words(i): i for i in range(10)},
        **{f"{i}": i for i in range(10)}
    }
    control_digits = [_get_control_digit(line) for line in INPUT]
    return sum(control_digits)


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
