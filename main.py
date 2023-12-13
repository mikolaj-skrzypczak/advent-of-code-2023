import importlib

# choose between 1 and 25
DAY = 13


def main() -> None:
    try:
        solution = importlib.import_module(f"solutions.{DAY:02d}")
    except ModuleNotFoundError:
        print(f"Solution for given day [{DAY}] not found.")
        return

    print(
        f"Puzzle description: https://adventofcode.com/2023/day/{DAY}\n"
        f"Answer given input from /inputs/{DAY:02d}.txt:"
    )
    solution.main()


if __name__ == '__main__':
    main()
