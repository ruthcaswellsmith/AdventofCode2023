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

NUM_CYCLES = 1000

class Pulse(str, Enum):
    HIGH = auto()
    LOW = auto()


class Module:
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        self.manager = manager
        self.id = identifier
        self.outputs = outputs

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
        super().send_pulse(Pulse.HIGH if self.on else Pulse.LOW)


class Conjunction(Module):
    def __init__(self, manager: ModuleManager, identifier: str, outputs: List[str]):
        super().__init__(manager, identifier, outputs)
        self.inputs: List[str] = []
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
        self.watcher = None
        self.found = False

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
                    if isinstance(output, Conjunction):
                        output.inputs.append(module.id)
                except:
                    unknown_outputs.append(identifier)
        for output in unknown_outputs:
            self.modules[output] = (OutputOnly(self, output, []))
        # Initialize our conjunctions
        for module in self.modules.values():
            if isinstance(module, Conjunction):
                module.most_recent_pulses = {i: Pulse.LOW for i in module.inputs}

    def push_button(self):
        self.queue.put((Pulse.LOW, BUTTON, BROADCASTER))
        while not self.queue.empty():
            pulse, source, dest = self.queue.get()
            if self.watcher(pulse, source, dest):
                self.found = True
            self.pulses[pulse] += 1
            self.modules[dest].process_pulse(pulse, source)


if __name__ == "__main__":
    filename = 'input/Day20.txt'
    data = read_file(filename)

    manager = ModuleManager(data)
    for i in range(NUM_CYCLES):
        manager.push_button()

    print(f"The answer to Part 1 is {np.prod(np.array(list(manager.pulses.values())))}")

    # For Part 2 we have an LCM number.  We know there is one conjunction module which
    # inputs to rx, and that has four conjunction modules as inputs.
    # So each of those needs to remember high for all its inputs in order to deliver a
    # low pulse to the conjunction module.  Then we find the LCM of those cycles

    # Find the conjunction module
    manager = ModuleManager(data)
    conjunction = next(iter([module.id for module in manager.modules.values() if module.outputs == ['rx']]))
    inputs = manager.modules[conjunction].inputs
    lcm = 1
    for id in inputs:
        num = 0
        manager = ModuleManager(data)
        manager.watcher = lambda pulse, source, dest: pulse == Pulse.HIGH and source == id and dest == conjunction
        while not manager.found:
            num += 1
            manager.push_button()
            # found = not all(value == Pulse.HIGH for value in manager.modules[id].most_recent_pulses.values())
        lcm *= num

    print(f"The answer to Part 2 is {lcm}")
