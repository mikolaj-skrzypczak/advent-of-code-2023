from utils.utils import print_solutions, load_input, get_all_numbers_in_string

INPUT = load_input(6)


def part_1() -> int:
    result = 1
    for time, distance in zip(*map(get_all_numbers_in_string, INPUT)):
        ways_to_win = get_ways_to_win_count(time, distance)
        result *= ways_to_win
    return result


def part_2() -> int:
    time = int("".join(get_all_numbers_in_string(INPUT[0], as_strings=True)))
    distance = int("".join(get_all_numbers_in_string(INPUT[1], as_strings=True)))
    return get_ways_to_win_count(time, distance)


def get_ways_to_win_count(time: int, distance: int) -> int:
    ways_to_win = 0
    for speed_per_second in range(time + 1):
        remaining_time = time - speed_per_second
        if remaining_time * speed_per_second > distance:
            ways_to_win += 1
    return ways_to_win


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
