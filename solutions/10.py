from utils.utils import print_solutions, load_input
from matplotlib.path import Path

GRID = list(map(list, load_input(10)))

FROM_LEFT = MOVE_RIGHT = (0, 1)
FROM_RIGHT = MOVE_LEFT = (0, -1)
FROM_TOP = MOVE_DOWN = (1, 0)
FROM_BOTTOM = MOVE_UP = (-1, 0)


def part_1() -> tuple[int, list[list[int, int]]]:
    starting_position = get_starting_position()
    tries = (MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT)
    for direction in tries:
        first_move = direction
        current_position = list(starting_position)
        path = [current_position]
        update_position(current_position, first_move)
        path.append(current_position[:])
        try:
            path_len, path = find_path(current_position, path, first_move)
            return path_len, path
        except (ValueError, KeyError):
            print(f"[p1] Failed going {direction}")


def part_2(path: list[list[int, int]]) -> int:
    enclosed = 0
    _path = Path(path)  # type: ignore
    for y in range(len(GRID)):
        for x in range(len(GRID[0])):
            if [x, y] in path:
                continue
            if _path.contains_point((x, y)):
                enclosed += 1
    return enclosed


def get_starting_position() -> tuple[int, int]:
    for y, row in enumerate(GRID):
        for x, char in enumerate(row):
            if char == "S":
                return y, x


def find_path(
        current_position: list[int, int], path: list[list[int, int]], first_move: tuple[int, int]
) -> tuple[int, list[list[int, int]]]:
    path_len = 1
    last_move = first_move
    while GRID[current_position[0]][current_position[1]] != "S":
        path.append(current_position[:])
        last_move = Pipe(GRID[current_position[0]][current_position[1]]).move(last_move, current_position)
        path_len += 1
    return path_len // 2, path


def update_position(current_position: list[int, int], move: tuple[int, int]) -> None:
    current_position[0], current_position[1] = current_position[0] + move[0], current_position[1] + move[1]


class Pipe:
    PIPES = {
        "|": {
            FROM_BOTTOM: MOVE_UP,
            FROM_TOP: MOVE_DOWN
        },
        "-": {
            FROM_LEFT: MOVE_RIGHT,
            FROM_RIGHT: MOVE_LEFT
        },
        "L": {
            FROM_RIGHT: MOVE_UP,
            FROM_TOP: MOVE_RIGHT
        },
        "J": {
            FROM_LEFT: MOVE_UP,
            FROM_TOP: MOVE_LEFT
        },
        "7": {
            FROM_LEFT: MOVE_DOWN,
            FROM_BOTTOM: MOVE_LEFT
        },
        "F": {
            FROM_RIGHT: MOVE_DOWN,
            FROM_BOTTOM: MOVE_RIGHT
        },
    }

    def __init__(self, pipe: str):
        self.pipe = pipe

    def move(self, last_move: tuple[int, int], current_position: list[int, int]) -> tuple[int, int]:
        current_pipe = GRID[current_position[0]][current_position[1]]
        if current_pipe not in self.PIPES:
            raise ValueError("Not a pipe")
        try:
            move = self.PIPES[current_pipe][last_move]
        except KeyError:
            raise ValueError("Not a valid move")
        update_position(current_position, move)
        return move


def main():
    p1, path = part_1()
    p2 = part_2(path)
    print_solutions(p1, p2)


if __name__ == '__main__':
    main()
