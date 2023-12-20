from __future__ import annotations
from abc import abstractmethod

from typing import Dict, List

from utils import read_file

BROADCASTER = 'broadcaster'

class Module:
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        self.manager = manager
        self.id = identifier
        self.outputs = outputs

    def send_pulse(self, pulse: bool):
        for output in self.outputs:
            self.manager.modules[output].receive_pulse(pulse, self.id)

    @abstractmethod
    def receive_pulse(self, pulse: bool, source: str):
        pass


class Broadcaster(Module):
    def __init__(self, manager: ModuleManager, outputs: List[str]):
        super().__init__(manager, BROADCASTER, outputs)

    def receive_pulse(self, pulse: bool, source: str):
        self.send_pulse(pulse)


class FlipFlop(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.state = False

    def receive_pulse(self, pulse: bool, source: str):
        if pulse:
            return None
        self.state = not self.state
        self.send_pulse(self.state)


class Conjunction(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.most_recent_pulses = {}

    def receive_pulse(self, pulse: bool, source: str):
        self.most_recent_pulses[source] = pulse
        pulse = False if all(self.most_recent_pulses.values()) else True
        self.send_pulse(pulse)

class ModuleManager:
    def __init__(self, data: List[str]):
        self.modules: Dict[id, Module] = self.get_modules(data)

    def get_modules(self, data: List[str]):
        modules = {}
        for line in data:
            pts = line.split(' -> ')
            outputs = [pt.strip() for pt in pts[1].split(',')]
            if BROADCASTER in line:
                modules[BROADCASTER] = Broadcaster(self, outputs)
            identifier = pts[0][1:]
            if pts[0][0] == '%':
                modules[identifier] = FlipFlop(self, identifier, outputs)
            else:
                modules[identifier] = Conjunction(self, identifier, outputs)
        return modules

    def populate_inputs(self):
        pass


if __name__ == "__main__":
    filename = 'input/test.txt'
    data = read_file(filename)

    manager = ModuleManager(data)

    print(f"The answer to Part 1 is {1}")

    print(f"The answer to Part 2 is {2}")
