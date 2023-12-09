from utils.utils import print_solutions, load_input, get_all_numbers_in_string

INPUT = list(map(get_all_numbers_in_string, load_input(9)))


def part_1() -> int:
    return sum(map(solve, INPUT))


def part_2() -> int:
    return sum(map(solve, [i[::-1] for i in INPUT]))


def solve(numbers: list[int]) -> int:
    if all(i == 0 for i in numbers):
        return 0
    return numbers[-1] + solve([j - i for i, j in zip(numbers, numbers[1:])])


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
