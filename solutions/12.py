from functools import cache

from utils.utils import print_solutions, load_input, get_all_numbers_in_string


def parse_input(_input: list[str]) -> list[tuple[str, tuple[int, ...]]]:
    return [(line.split(" ")[0], tuple(get_all_numbers_in_string(line))) for line in _input]


INPUT = parse_input(load_input(12))
DAMAGED = "#"
OPERATIONAL = "."
WILDCARD = "?"


def part_1() -> int:
    return sum(solve(sequence + ".", criteria) for sequence, criteria in INPUT)


def part_2() -> int:
    return sum(solve("?".join([sequence] * 5) + ".", criteria * 5) for sequence, criteria in INPUT)


@cache
def solve(row: str, spring_sequences: tuple[int, ...], sequence_length: int = 0) -> int:
    if not row:
        return 1 if not spring_sequences and sequence_length == 0 else 0

    n = 0
    if row.startswith(DAMAGED) or row.startswith(WILDCARD):
        n += solve(row[1:], spring_sequences, sequence_length + 1)
    if (row.startswith(WILDCARD) or row.startswith(OPERATIONAL)) and _are_valid(spring_sequences, sequence_length):
        if sequence_length != 0:
            n += solve(row[1:], spring_sequences[1:], 0)
        else:
            n += solve(row[1:], spring_sequences, 0)
    return n


def _are_valid(sequences: tuple[int, ...], current_sequence_len: int) -> bool:
    def _is_valid_sequence(_sequences: tuple[int, ...], _current_sequence_len: int) -> bool:
        return _sequences and _sequences[0] == _current_sequence_len

    return _is_valid_sequence(sequences, current_sequence_len) or current_sequence_len == 0


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
