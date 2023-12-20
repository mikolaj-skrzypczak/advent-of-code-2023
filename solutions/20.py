from __future__ import annotations

from abc import ABC, abstractmethod
from math import lcm

from utils.utils import print_solutions, load_input

LOW_SIGNAL = 0
HIGH_SIGNAL = 1


class Module(ABC):
    raw_receivers: list[str]
    receivers_references: list[Module]

    def __init__(self, _input_line) -> None:
        if " -> " not in _input_line:
            self.name = _input_line
        else:
            self.receivers_references = []
            self.name = _input_line.split(" -> ")[0][1:] if not _input_line.startswith("broadcaster") else "broadcaster"
            self.raw_receivers = _input_line.split(" -> ")[1].split(", ")

    def connect(self, modules: dict[str, Module]) -> None:
        if self.raw_receivers[0] == "":
            return
        for receiver in self.raw_receivers:
            if receiver == "rx":
                self.receivers_references.append(FinalReceiver(receiver))
                continue
            self.receivers_references.append(modules[receiver])

    @abstractmethod
    def receive(self, signal: int, sender: Module) -> None:
        pass

    @abstractmethod
    def prepare_calls(self, calls_counter: dict[int, int], push_num: int) -> list[tuple[Module, Module, int]]:
        pass


class Broadcaster(Module):
    def __init__(self, _input_line) -> None:
        super().__init__(_input_line)
        self.signal_to_send = LOW_SIGNAL

    def receive(self, signal: int, sender: Module) -> None:
        ...

    def prepare_calls(self, calls_counter: dict[int, int], _: int) -> list[tuple[Module, Module, int]]:
        calls = []
        for receiver in self.receivers_references:
            calls_counter[self.signal_to_send] += 1
            calls.append((receiver, self, self.signal_to_send))

        return calls


class FlipFlop(Module):
    def __init__(self, _input_line) -> None:
        super().__init__(_input_line)
        self.is_on = False
        self.signal_to_send = None

    def receive(self, signal: int, sender: Module) -> None:
        if signal == HIGH_SIGNAL:
            self.signal_to_send = None
            return
        self.is_on = not self.is_on
        if self.is_on:
            self.signal_to_send = HIGH_SIGNAL
        else:
            self.signal_to_send = LOW_SIGNAL

    def prepare_calls(self, calls_counter: dict[int, int], _: int) -> list[tuple[Module, Module, int]]:
        calls = []
        if self.signal_to_send is None:
            return []
        for receiver in self.receivers_references:
            calls_counter[self.signal_to_send] += 1
            calls.append((receiver, self, self.signal_to_send))
        return calls


class Conjunction(Module):

    def __init__(self, _input_line) -> None:
        super().__init__(_input_line)
        self.last_received = dict()

    def receive(self, signal: int, sender: Module) -> None:
        self.last_received[sender.name] = signal

    def prepare_calls(self, calls_counter: dict[int, int], push_num: int) -> list[tuple[Module, Module, int]]:
        calls = []
        if all(self.last_received.values()):
            for receiver in self.receivers_references:
                calls_counter[LOW_SIGNAL] += 1
                calls.append((receiver, self, LOW_SIGNAL))
        else:
            if self in PENULTIMATE_CONJUNCTIONS and self not in PENULTIMATE_CONJUNCTION_SENT_HIGH_TO_PUSH_NUM:
                PENULTIMATE_CONJUNCTION_SENT_HIGH_TO_PUSH_NUM[self] = push_num
            for receiver in self.receivers_references:
                calls_counter[HIGH_SIGNAL] += 1
                calls.append((receiver, self, HIGH_SIGNAL))
        return calls


class FinalReceiver(Module):
    def __init__(self, _input_line) -> None:
        super().__init__(_input_line)
        self.last_received = None

    def receive(self, signal: int, sender: Module) -> None:
        if signal == LOW_SIGNAL:
            raise Exception("Final receiver received LOW")

    def prepare_calls(self, calls_counter: dict[int, int], push_num: int) -> list[tuple[Module, Module, int]]:
        return []


def parse_input_to_modules(_input: list[str]) -> dict[str, Module]:
    modules = {}
    type_to_class = {
        "%": FlipFlop,
        "&": Conjunction
    }
    for line in _input:
        if line.startswith("broadcaster"):
            modules["broadcaster"] = Broadcaster(line)
        else:
            module_type_and_name = line.split(" -> ")[0]
            modules[module_type_and_name[1:]] = type_to_class[module_type_and_name[0]](line)
    modules["output"] = Conjunction("output -> ")

    for module in modules.values():
        module.connect(modules)

    for module in modules.values():
        for receiver in module.receivers_references:
            if isinstance(receiver, Conjunction):
                receiver.last_received[module.name] = LOW_SIGNAL

    return modules


def get_penultimate_conjunctions(modules: dict[str, Module]) -> list[Module]:
    final_conjunction = None
    for module in modules.values():
        for receiver in module.receivers_references:
            if isinstance(receiver, FinalReceiver):
                final_conjunction = module
                break
    modules_sending_to_final_conjunction = []
    for module in modules.values():
        for receiver in module.receivers_references:
            if receiver == final_conjunction:
                modules_sending_to_final_conjunction.append(module)
    return modules_sending_to_final_conjunction


MODULES = parse_input_to_modules(load_input(20))
PENULTIMATE_CONJUNCTIONS = get_penultimate_conjunctions(MODULES)
PENULTIMATE_CONJUNCTION_SENT_HIGH_TO_PUSH_NUM = {}


def part_1() -> int:
    calls_counter = {
        LOW_SIGNAL: 0,
        HIGH_SIGNAL: 0
    }

    for _ in range(1000):
        push_button(calls_counter, 0)

    return calls_counter[LOW_SIGNAL] * calls_counter[HIGH_SIGNAL]


def part_2() -> int:
    def should_finish():
        return all(
            module in PENULTIMATE_CONJUNCTION_SENT_HIGH_TO_PUSH_NUM
            for module in PENULTIMATE_CONJUNCTIONS
        )

    push_num = 0
    while not should_finish():
        push_num += 1
        push_button({LOW_SIGNAL: 0, HIGH_SIGNAL: 0}, push_num)
    return lcm(*PENULTIMATE_CONJUNCTION_SENT_HIGH_TO_PUSH_NUM.values())


def push_button(calls_counter: dict[int, int], push_num: int) -> None:
    calls = MODULES["broadcaster"].prepare_calls(calls_counter, push_num)
    calls_counter[LOW_SIGNAL] += 1
    while calls:
        new_calls = []
        for receiver, sender, signal in calls:
            receiver.receive(signal, sender)
            new_calls += receiver.prepare_calls(calls_counter, push_num)
        calls = new_calls


def main() -> None:
    print_solutions(part_1(), part_2())


if __name__ == "__main__":
    main()
