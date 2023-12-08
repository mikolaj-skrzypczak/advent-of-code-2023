import re
from typing import Callable
from math import lcm

from utils.utils import load_input, print_solutions


def parse_nodes(nodes: list[str]) -> dict[str, tuple[str, ...]]:
    nodes_dict = {}
    for node in nodes:
        node_name, left, right = LINE_RE.match(node).groups()
        nodes_dict[node_name] = (left, right)
    return nodes_dict


INPUT = load_input(8)
RIGHT = "R"
LEFT = "L"
LINE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")
INSTRUCTIONS = INPUT[0]
NODES = parse_nodes(INPUT[2:])


def part_1() -> int:
    starting_node = "AAA"
    return traverse(starting_node, lambda x: x == "ZZZ")


def part_2() -> int:
    starting_nodes = [node for node in NODES.keys() if node.endswith("A")]
    steps = [traverse(node, lambda x: x.endswith("Z")) for node in starting_nodes]
    return lcm(*steps)


def traverse(starting_node: str, stop_condition: Callable[[str], bool]) -> int:
    steps = 0
    curr_node = starting_node
    while not stop_condition(curr_node):
        curr_node = do_step(curr_node, steps)
        steps += 1
    return steps


def do_step(node: str, step: int) -> str:
    instruction = INSTRUCTIONS[step % len(INSTRUCTIONS)]
    if instruction == RIGHT:
        return NODES[node][1]
    elif instruction == LEFT:
        return NODES[node][0]


def main():
    print_solutions(part_1(), part_2())


if __name__ == '__main__':
    main()
