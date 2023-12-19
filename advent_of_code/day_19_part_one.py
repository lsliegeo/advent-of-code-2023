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

    def applies(self, values: dict) -> bool:
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

    def applies(self, values: dict) -> bool:
        return eval(f'{values[self.variable]}{self.operator}{self.value}')


@dataclasses.dataclass
class DefaultRule(Rule):

    def applies(self, values: dict) -> bool:
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

    def evaluate(self, part: dict) -> str:
        for rule in self.rules:
            if rule.applies(part):
                return rule.result
        raise Exception('No matching rule found')


def part1(input_data: str):
    workflows: list[Workflow] = [Workflow.from_string(line) for line in input_data.split('\n\n')[0].splitlines()]
    workflows: dict[str, Workflow] = {w.name: w for w in workflows}

    parts: list[dict] = [
        {
            assignment.split('=')[0]: int(assignment.split('=')[1])
            for assignment in line[1:-1].split(',')
        }
        for line in input_data.split('\n\n')[1].splitlines()
    ]

    result = 0
    for part in parts:
        output = 'in'
        while output not in 'RA':
            output = workflows[output].evaluate(part)
        if output == 'A':
            result += sum(part.values())
    return result


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 19114
    print(f'Solution for part 1 is: {part1(get_input())}')
