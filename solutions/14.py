import copy

import numpy as np

from utils.utils import print_solutions, load_input

MATRIX = np.array(list(map(list, load_input(14))))

SLIDING_ROCK = "O"
BLOCKER = "#"
EMPTY = "."


def part_1() -> int:
    matrix = copy.deepcopy(MATRIX)
    slide_rocks_north(matrix)
    return calculate_load(matrix)


def part_2() -> int:
    seen_matrices = push_and_rotate_until_cycle_found(copy.deepcopy(MATRIX))
    matrix = get_array_at_desired_index(seen_matrices, 10 ** 9)
    return calculate_load(matrix)


def slide_rocks_north(matrix: np.ndarray) -> None:
    for y in range(1, len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == SLIDING_ROCK:
                last_blocker = get_last_blocker(matrix, (y, x))
                if y != last_blocker:
                    matrix[y][x] = EMPTY
                    matrix[last_blocker][x] = SLIDING_ROCK


def get_last_blocker(matrix: np.ndarray, current_position: tuple[int, int]) -> int:
    for y in range(current_position[0], -1, -1):
        if matrix[y - 1][current_position[1]] in (BLOCKER, SLIDING_ROCK):
            return y
    return 0


def calculate_load(matrix: np.ndarray) -> int:
    result = 0
    m_len = len(matrix)
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == SLIDING_ROCK:
                result += m_len - y
    return result


def push_and_rotate_until_cycle_found(matrix: np.ndarray) -> list[list[list[str]]]:
    seen = []
    while True:
        matrix = get_new_matrix_after_cycle(matrix)
        if matrix.tolist() not in seen:
            seen.append(copy.deepcopy(matrix.tolist()))
        else:
            seen.append(copy.deepcopy(matrix.tolist()))
            break
    return seen


def get_new_matrix_after_cycle(matrix: np.ndarray) -> np.ndarray:
    for _ in range(4):
        slide_rocks_north(matrix)
        matrix = rotate_clockwise(matrix)
    return matrix


def rotate_clockwise(matrix: np.ndarray) -> np.ndarray:
    return np.rot90(matrix, k=3)


def get_array_at_desired_index(seen: list[list[list[str]]], desired_index: int) -> np.ndarray:
    cycle_start = seen.index(seen.pop())
    reminder = (desired_index - cycle_start) % (len(seen) - cycle_start)
    return np.array(seen[cycle_start + reminder - 1])


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
