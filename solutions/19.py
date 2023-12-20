import copy
import math
import re
from collections import deque
from typing import NamedTuple, Optional

from utils.utils import print_solutions, load_input

WORKFLOW_NAME_RE = re.compile(r"(\w+){")
WORKFLOW_ELSE_CONDITION_RE = re.compile(r"(\w+)}")
WORKFLOW_RULE_RE = re.compile(r"(\w+)([<>])(\d+):(\w+),")
RATING_REGEXP = re.compile(r"([a-z]+)=(\d+)")
Rule = NamedTuple("Rule", [("category", str), ("operator", str), ("value", int), ("goto", str)])


def parse_ratings(original_ratings: list[str]) -> list[dict[str, str]]:
    return [dict(RATING_REGEXP.findall(rating)) for rating in original_ratings]


def parse_workflows(original_workflows: list[str]) -> dict[str, dict[str, str | list[tuple[str, str, int]]]]:
    workflows = {}
    for workflow in original_workflows:
        name, rules, else_condition = parse_workflow(workflow)
        workflows[name] = {"rules": rules, "else_condition": else_condition}
    return workflows


def parse_workflow(original_workflow: str) -> tuple[str, list[Rule], str]:
    name = WORKFLOW_NAME_RE.findall(original_workflow)[0]
    else_condition = WORKFLOW_ELSE_CONDITION_RE.findall(original_workflow)[0]
    rules = [Rule(*r) for r in WORKFLOW_RULE_RE.findall(original_workflow)]
    return name, rules, else_condition


INPUT = load_input(19)
WORKFLOWS = parse_workflows(INPUT[:INPUT.index("")])
RATINGS_OF_PARTS = parse_ratings(INPUT[INPUT.index("") + 1:])
ACCEPTED = "A"
REJECTED = "R"


def part_1() -> int:
    return sum(evaluate_part_rating(part_rating) for part_rating in RATINGS_OF_PARTS)


def part_2() -> int:
    xmas_ranges = {c: [1, 4000] for c in "xmas"}
    return find_n_of_xmas_combinations_leading_to_acceptance(xmas_ranges)


def evaluate_part_rating(part_rating: dict[str, str]) -> int:
    workflow_name = "in"
    while workflow_name != ACCEPTED and workflow_name != REJECTED:
        workflow = WORKFLOWS[workflow_name]
        for rule in workflow["rules"]:
            if is_true(rule, part_rating[rule.category]):
                workflow_name = rule.goto
                break
        else:
            workflow_name = workflow["else_condition"]
    if workflow_name == ACCEPTED:
        return sum(int(part_rating[part]) for part in part_rating)
    return 0


def is_true(rule: Rule, rating: str) -> Optional[bool]:
    if rule.operator == "<":
        return int(rating) < int(rule.value)
    elif rule.operator == ">":
        return int(rating) > int(rule.value)


def find_n_of_xmas_combinations_leading_to_acceptance(xmas_ranges: dict[str, list[int]]) -> int:
    result = 0
    dq = deque([("in", copy.deepcopy(xmas_ranges))])
    while dq:
        current_workflow_name, current_ranges = dq.popleft()
        if any(current_ranges[c][0] > current_ranges[c][1] for c in current_ranges):
            continue
        if current_workflow_name == ACCEPTED:
            result += math.prod(current_ranges[c][1] - current_ranges[c][0] + 1 for c in current_ranges)
            continue
        if current_workflow_name == REJECTED:
            continue
        current_workflow = WORKFLOWS[current_workflow_name]
        for rule in current_workflow["rules"]:
            dq.append((rule.goto, get_updated_ranges_on_successful_rule(current_ranges, rule)))
            current_ranges = get_updated_ranges_on_failed_rule(current_ranges, rule)
        dq.append((current_workflow["else_condition"], copy.deepcopy(current_ranges)))
    return result


def get_updated_ranges_on_successful_rule(current_ranges: dict[str, list[int]], rule: Rule) -> dict[str, list[int]]:
    new_ranges = copy.deepcopy(current_ranges)
    if rule.operator == "<":
        new_ranges[rule.category][1] = min(current_ranges[rule.category][1], int(rule.value) - 1)
    elif rule.operator == ">":
        new_ranges[rule.category][0] = max(current_ranges[rule.category][0], int(rule.value) + 1)
    return new_ranges


def get_updated_ranges_on_failed_rule(current_ranges: dict[str, list[int]], rule: Rule) -> dict[str, list[int]]:
    new_ranges = copy.deepcopy(current_ranges)
    if rule.operator == "<":
        new_ranges[rule.category][0] = max(current_ranges[rule.category][0], int(rule.value))
    elif rule.operator == ">":
        new_ranges[rule.category][1] = min(current_ranges[rule.category][1], int(rule.value))
    return new_ranges


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == "__main__":
    main()
