from __future__ import annotations

import abc
import dataclasses
import re

from util.input_util import get_input

EXAMPLE = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


@dataclasses.dataclass
class Rule(abc.ABC):
    result: str

    @abc.abstractmethod
    def applies(self, values: dict[str, int]) -> bool:
        raise NotImplementedError()

    @classmethod
    def from_string(cls, s: str) -> Rule:
        if match := re.match('([a-z]+)(.)(\d+):([A-z]+)', s):
            return ConditionalRule(
                match.group(4),
                match.group(1),
                match.group(2),
                int(match.group(3)),
            )
        else:
            return DefaultRule(s)


@dataclasses.dataclass
class ConditionalRule(Rule):
    variable: str
    operator: str
    value: int

    def applies(self, values: dict[str, int]) -> bool:
        return eval(f'{values[self.variable]}{self.operator}{self.value}')


@dataclasses.dataclass
class DefaultRule(Rule):

    def applies(self, values: dict[str, int]) -> bool:
        return True


@dataclasses.dataclass
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def from_string(cls, s: str) -> Workflow:
        match = re.match('(.*){(.*)}', s)
        return cls(
            match.group(1),
            [Rule.from_string(rule_string) for rule_string in match.group(2).split(',')]
        )

    def evaluate(self, lower: dict[str, int], upper: dict[str, int]) -> list[tuple[str, dict[str, int], dict[str, int]]]:
        result = []
        for rule in self.rules:
            if rule.applies(lower) and rule.applies(upper):
                result.append((rule.result, lower, upper))
            elif isinstance(rule, ConditionalRule):
                if rule.operator == '<':
                    if lower[rule.variable] < rule.value:
                        result.append((rule.result, lower, upper | {rule.variable: rule.value - 1}))
                        lower = lower | {rule.variable: rule.value}
                else:
                    if upper[rule.variable] > rule.value:
                        result.append((rule.result, lower | {rule.variable: rule.value + 1}, upper))
                        upper = upper | {rule.variable: rule.value}
            else:
                raise Exception('Unexpected condition range')
        return result


def part2(input_data: str):
    workflows = [Workflow.from_string(line) for line in input_data.split('\n\n')[0].splitlines()]
    workflows = {w.name: w for w in workflows}
    inputs = [('in', {x: 1 for x in 'xmas'}, {x: 4000 for x in 'xmas'})]
    result = 0
    for lower, upper in sort_ranges(workflows, inputs):
        additional = 1
        for x in 'xmas':
            additional *= upper[x] - lower[x] + 1
        result += additional
    return result


def sort_ranges(workflows: dict[str, Workflow], inputs: list[tuple[str, dict[str, int], dict[str, int]]]) -> list[tuple[dict[str, int], dict[str, int]]]:
    accepted_ranges = []
    while inputs:
        current_workflow_name, current_lower, current_upper = inputs.pop()
        for output, next_lower, next_upper in workflows[current_workflow_name].evaluate(current_lower, current_upper):
            if output == 'A':
                accepted_ranges.append((next_lower, next_upper))
            elif output != 'R':
                inputs.append((output, next_lower, next_upper))
    return accepted_ranges


if __name__ == '__main__':
    assert part2(EXAMPLE) == 167409079868000
    print(f'Solution for part 2 is: {part2(get_input())}')
