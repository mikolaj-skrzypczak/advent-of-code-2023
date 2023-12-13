from collections import Counter
from typing import Callable

from utils.utils import print_solutions, load_input

INPUT = load_input(7)

HANDS_STRENGTH = {
    "high card": 1,
    "one pair": 2,
    "two pairs": 3,
    "three of a kind": 4,
    "full house": 5,
    "four of a kind": 6,
    "five of a kind": 7
}

CARDS_STRENGTH = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13
}


def part_1() -> int:
    return solve(determine_hand_strength)


def part_2() -> int:
    CARDS_STRENGTH["J"] = 0
    return solve(try_find_best_hand_with_joker_wildcards)


def solve(determine_hand_strength_function: Callable) -> int:
    def parse_input() -> list[tuple]:
        _hands = []
        for line in INPUT:
            cards, bid = line.split(" ")
            cards = [CARDS_STRENGTH[_i] for _i in list(cards)]
            _hands.append((cards, determine_hand_strength_function(cards), int(bid)))
        return _hands

    result = 0
    hands = parse_input()
    hands.sort(key=lambda x: (x[1], x[0]))
    for i, hand in enumerate(hands, start=1):
        result += hand[2] * i
    return result


def determine_hand_strength(cards: list[int]) -> int:
    counter = Counter(cards)
    if len(counter) == 1:
        return HANDS_STRENGTH["five of a kind"]
    if len(counter) == 2:
        if 4 in counter.values():
            return HANDS_STRENGTH["four of a kind"]
        return HANDS_STRENGTH["full house"]
    if len(counter) == 3:
        if 3 in counter.values():
            return HANDS_STRENGTH["three of a kind"]
        return HANDS_STRENGTH["two pairs"]
    if len(counter) == 4:
        return HANDS_STRENGTH["one pair"]
    return HANDS_STRENGTH["high card"]


def try_find_best_hand_with_joker_wildcards(cards: list[int]) -> int:
    def try_find_best_hand_with_one_joker_wildcard() -> int:
        if len(counter) == 2:
            return HANDS_STRENGTH["five of a kind"]
        if len(counter) == 3:
            if 3 in counter.values():
                return HANDS_STRENGTH["four of a kind"]
            return HANDS_STRENGTH["full house"]
        if len(counter) == 4:
            return HANDS_STRENGTH["three of a kind"]
        return HANDS_STRENGTH["one pair"]

    def try_find_best_hand_with_two_joker_wildcards() -> int:
        if len(counter) == 2:
            return HANDS_STRENGTH["five of a kind"]
        if len(counter) == 3:
            return HANDS_STRENGTH["four of a kind"]
        if len(counter) == 4:
            return HANDS_STRENGTH["three of a kind"]

    def try_find_best_hand_with_three_joker_wildcards() -> int:
        if len(counter) == 2:
            return HANDS_STRENGTH["five of a kind"]
        if len(counter) == 3:
            return HANDS_STRENGTH["four of a kind"]

    def try_find_best_hand_with_four_joker_wildcards() -> int:
        return HANDS_STRENGTH["five of a kind"]

    def try_find_best_hand_with_five_joker_wildcards() -> int:
        return HANDS_STRENGTH["five of a kind"]

    counter = Counter(cards)
    if 0 not in counter:
        return determine_hand_strength(cards)
    return {
        1: try_find_best_hand_with_one_joker_wildcard,
        2: try_find_best_hand_with_two_joker_wildcards,
        3: try_find_best_hand_with_three_joker_wildcards,
        4: try_find_best_hand_with_four_joker_wildcards,
        5: try_find_best_hand_with_five_joker_wildcards
    }[counter.get(0)]()


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
