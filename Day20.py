from __future__ import annotations

from abc import abstractmethod
from enum import Enum, auto
from typing import Dict, List
import numpy as np
from queue import Queue

from utils import read_file

BROADCASTER = 'broadcaster'
BUTTON = 'button'
OUTPUT = 'output'


class Pulse(str, Enum):
    HIGH = auto()
    LOW = auto()


class Module:
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        self.manager = manager
        self.id = identifier
        self.outputs = outputs
        self.inputs: List[str] = []

    def send_pulse(self, pulse: Pulse):
        for output in self.outputs:
            self.manager.queue.put((pulse, self.id, output))

    @abstractmethod
    def process_pulse(self, pulse: Pulse, source: str):
        pass


class Broadcaster(Module):
    def __init__(self, manager: ModuleManager, outputs: List[str]):
        super().__init__(manager, BROADCASTER, outputs)

    def process_pulse(self, pulse: Pulse, source: str):
        super().send_pulse(pulse)


class FlipFlop(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.on = False

    def process_pulse(self, pulse: Pulse, source: str):
        if pulse == Pulse.HIGH:
            return
        self.on = not self.on
        super().send_pulse(
            Pulse.HIGH if self.on else Pulse.LOW
        )


class Conjunction(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.most_recent_pulses = {}

    def process_pulse(self, pulse: Pulse, source: str):
        self.most_recent_pulses[source] = pulse
        super().send_pulse(
            Pulse.LOW if \
                all(value == Pulse.HIGH for value in self.most_recent_pulses.values()) else \
                Pulse.HIGH
        )


class OutputOnly(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.saved = None

    def process_pulse(self, pulse: Pulse, source: str):
        self.saved = pulse


class ModuleManager:
    def __init__(self, data: List[str]):
        self.modules: Dict[id, Module] = self.get_modules(data)
        self.populate_inputs()
        self.queue = Queue()
        self.pulses = {Pulse.HIGH: 0, Pulse.LOW: 0}

    def get_modules(self, data: List[str]):
        modules = {}
        for line in data:
            pts = line.split(' -> ')
            outputs = [pt.strip() for pt in pts[1].split(',')]
            if BROADCASTER in line:
                modules[BROADCASTER] = Broadcaster(self, outputs)
                continue
            identifier = pts[0][1:]
            if pts[0][0] == '%':
                modules[identifier] = FlipFlop(self, identifier, outputs)
            else:
                modules[identifier] = Conjunction(self, identifier, outputs)
        return modules

    def populate_inputs(self):
        unknown_outputs = []
        for module in self.modules.values():
            for identifier in module.outputs:
                try:
                    output = self.modules[identifier]
                    output.inputs.append(module.id)
                except:
                    unknown_outputs.append(identifier)
            # if isinstance(module, Conjunction):
            #     module.most_recent_pulses = {i: Pulse.LOW for i in module.inputs}
        for output in unknown_outputs:
            self.modules[output] = (OutputOnly(self, output, []))

    def push_button(self):
        self.queue.put((Pulse.LOW, BUTTON, BROADCASTER))
        while not self.queue.empty():
            pulse, source, dest = self.queue.get()
            self.pulses[pulse] += 1
            self.modules[dest].process_pulse(pulse, source)


if __name__ == "__main__":
    filename = 'input/Day20.txt'
    data = read_file(filename)

    manager = ModuleManager(data)
    for i in range(1000):
        manager.push_button()

    print(f"The answer to Part 1 is {np.prod(np.array(list(manager.pulses.values())))}")

    print(f"The answer to Part 2 is {2}")
