import networkx as nx

from utils.utils import load_input

INPUT = load_input(25)

"""
Tried bruteforcing it using combinations and getting each remove-3-edges possibility and then
checking whether there are exactly 2 connected_components, but it failed miserably 
(although working for the test input), as there are 5 967 745 840 combinations of 3 edges to remove.
Found hint about the existence nx.minimum_edge_cut method on the subreddit, then the problem became trivial.
"""


def part_1() -> int:
    graph = nx.Graph(parse_input_to_edges())
    graph.remove_edges_from(nx.minimum_edge_cut(graph))
    subgraph_1, subgraph_2 = list(nx.connected_components(graph))
    return len(subgraph_1) * len(subgraph_2)


def parse_input_to_edges() -> set[tuple[str, str]]:
    return {
        (line.split(": ")[0], _to)
        for line in INPUT
        for _to in line.split(": ")[1].split()
    }


def main() -> None:
    print(f"Part 1: {part_1()}")
    print("No part 2! Merry Christmas!")


if __name__ == '__main__':
    main()
