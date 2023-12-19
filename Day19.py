from __future__ import annotations

import json
from math import prod
from typing import Callable, Union, Dict, Tuple, List

from utils import read_file, Part


class StateRange:
    def __init__(self, x: range, m: range, a: range, s: range):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @property
    def combinations(self):
        return prod(getattr(self, attr).stop - getattr(self, attr).start for attr in ['x', 'm', 'a', 's'])

    @staticmethod
    def split_range(r: range, value: int, comparison: str) -> \
            Tuple[Union[range, None], Union[range, None]]:
        if value in r:
            if comparison == '<':
                r1, r2 = range(r.start, value), range(value, r.stop)
            else:
                r1, r2 = range(value + 1, r.stop), range(r.start, value + 1)
            return r1 if len(r1) > 0 else None, r2 if len(r2) > 0 else None

        if comparison == '<':
            return (r, None) if value >= r.stop else (None, r)
        else:
            return (None, r) if value >= r.stop else (r, None)

    def split(self, condition: Condition) -> Tuple[Union[None, StateRange], Union[None, StateRange]]:
        attr_range = getattr(self, condition.variable)
        r1, r2 = self.split_range(attr_range, condition.value, condition.comparison)

        if condition.variable == 'x':
            return (
                StateRange(r1, self.m, self.a, self.s) if r1 else None,
                StateRange(r2, self.m, self.a, self.s) if r2 else None
            )
        elif condition.variable == 'm':
            return (
                StateRange(self.x, r1, self.a, self.s),
                StateRange(self.x, r2, self.a, self.s)
            )
        elif condition.variable == 'a':
            return (
                StateRange(self.x, self.m, r1, self.s),
                StateRange(self.x, self.m, r2, self.s)
            )
        else:
            return (
                StateRange(self.x, self.m, self.a, r1),
                StateRange(self.x, self.m, self.a, r2)
            )


class Condition:
    def __init__(self, text: str):
        self.comparison = "<" if "<" in text else ">"
        pts = text.split(self.comparison)
        self.variable, self.value = pts[0], int(pts[1])


class Rule:
    def __init__(self, condition: Callable,
                 outcome_true: Union[Rule, str],
                 outcome_false: Union[Rule, str]):
        self.condition = condition
        self.outcome_true = outcome_true
        self.outcome_false = outcome_false


class Rule2:
    def __init__(self, condition: Condition,
                 outcome_true: Union[Rule2, str],
                 outcome_false: Union[Rule2, str]):
        self.condition = condition
        self.outcome_true = outcome_true
        self.outcome_false = outcome_false


class Graph:
    def __init__(self, workflows: Dict[str], part: Part):
        self.part = part
        self.workflows = workflows
        self.rule_one = self.populate_rules(workflows['in'])

    def populate_rules(self, rule_text):
        if not ('<' in rule_text or '>' in rule_text):
            return self.populate_rules(self.workflows[rule_text])

        ind = rule_text.find(':')
        if ind < 0:
            raise ValueError('oops no colon')
        condition = self.text_to_lambda(rule_text[:ind]) if self.part == Part.PT1 else \
            Condition(rule_text[:ind])
        new_rule_text = rule_text[ind+1:]

        ind = new_rule_text.find(',')
        if ind < 0:
            raise ValueError('oops no comma')
        left = new_rule_text[:ind]
        right = new_rule_text[ind+1:]

        if left in ['A', 'R']:
            outcome_true = left
        elif ',' in left:
            outcome_true = self.populate_rules(left)
        else:
            outcome_true = self.populate_rules(self.workflows[left])

        if right in ['A', 'R']:
            outcome_false = right
        elif ',' in right:
            outcome_false = self.populate_rules(right)
        else:
            outcome_false = self.populate_rules(self.workflows[right])

        if self.part == Part.PT1:
            return Rule(condition, outcome_true, outcome_false)
        else:
            return Rule2(condition, outcome_true, outcome_false)

    @staticmethod
    def text_to_lambda(text: str) -> Callable:
        comparison = "<" if "<" in text else ">"
        pts = text.split(comparison)
        variable, value = pts[0], pts[1]

        return lambda state: eval(f"state['{variable}'] {comparison} {value}")

    def traverse(self, rule, state):
        if rule in ['A', 'R']:
            return rule

        if rule.condition(state):
            return self.traverse(rule.outcome_true, state)
        else:
            return self.traverse(rule.outcome_false, state)

    def traverse2(self, rule: Rule2, state_range: StateRange,
                  accepted: List[StateRange], rejected: List[StateRange]):
        if not state_range:
            return [], []

        if rule == 'A':
            return [state_range], []
        elif rule == 'R':
            return [], [state_range]

        true_range, false_range = state_range.split(rule.condition)

        left_accepted, left_rejected = \
            self.traverse2(rule.outcome_true, true_range, accepted, rejected)

        right_accepted, right_rejected = \
            self.traverse2(rule.outcome_false, false_range, accepted, rejected)

        return accepted + left_accepted + right_accepted, \
           rejected + left_rejected + right_rejected


if __name__ == "__main__":
    filename = 'input/Day19.txt'
    data = read_file(filename)

    workflows = {}
    for i in range(len(data)):
        if not data[i]:
            break
        pts = data[i].split('{')
        workflows[pts[0]] = pts[1].replace('}', '')

    # Part 1
    initial_states = [json.loads(data[j].replace('=', '":').replace('{', '{"').replace(',', ',"'))
              for j in range(i + 1, len(data))]
    graph = Graph(workflows, Part.PT1)
    accepted = [state for state in initial_states if graph.traverse(graph.rule_one, state) == 'A']
    print(f"The answer to Part 1 is {sum([sum(state.values()) for state in accepted])}")

    # Part 2
    initial_range = StateRange(range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))
    graph = Graph(workflows, Part.PT2)
    accepted, rejected = graph.traverse2(graph.rule_one, initial_range, [], [])
    print(f"The answer to Part 2 is {sum([a.combinations for a in accepted])}")
