import re
from typing import NamedTuple

from utils.utils import load_raw_input

INPUT = load_raw_input(5)
INPUT = INPUT.split("\n\n")

MapRange = NamedTuple("map_range", [("destination_range", int), ("source_range", int), ("range_length", int)])

map_to_x_re = r"(\d+) (\d+) (\d+)"


def part_1() -> int:
    seeds = list(map(int, INPUT[0].split(":")[1].strip().split(" ")))
    return min(chain_transformations(seeds))


def part_2() -> int:
    def split_list_into_chunks(_list: list, chunk_size: int) -> list[list]:
        return [_list[i:i + chunk_size] for i in range(0, len(_list), chunk_size)]

    results = []
    _input = INPUT[0].split(":")[1].strip().split(" ")
    seed_ranges = [range(int(i), int(i) + int(j)) for i, j in zip(_input[::2], _input[1::2])]
    for i, _range in enumerate(seed_ranges):
        seeds = list(_range)
        for j, chunk in enumerate(split_list_into_chunks(seeds, 1000)):
            if j % 1000 == 0:
                print(f"Processing chunk {j}/{len(seeds) // 1000} of seeds {i}/{len(seed_ranges)-1}")
            results.append(min(chain_transformations(chunk)))
        results = [min(results)]
    return results[0]


def chain_transformations(seeds: list[int]) -> list[int]:
    numbers = seeds
    for i, _map in enumerate(INPUT[1:]):
        maps = parse_map(_map)
        numbers = transform_based_on_map(numbers, maps)
    return numbers


def transform_based_on_map(numbers: list[int], maps: list[MapRange]) -> list[int]:
    def get_new_number(_number: int) -> int:
        for _map in maps:
            if _map.source_range <= _number <= _map.source_range + _map.range_length:
                return _map.destination_range + _number - _map.source_range
        return _number

    new_numbers = []
    for number in numbers:
        new_numbers.append(get_new_number(number))

    return new_numbers


def parse_map(_map: str) -> list[MapRange]:
    def to_named_tuple(t: tuple) -> MapRange:
        return MapRange(*(int(i) for i in t))

    return list(map(to_named_tuple, re.findall(map_to_x_re, _map)))


def main():
    print(f"Part 1: {part_1()}")
    print("Part 2 is being processed... (don't wait, it takes a really long time")
    print(f"Part 2: {part_2()}")


if __name__ == '__main__':
    main()
