from __future__ import annotations

import abc
import dataclasses

from util.input_util import get_input

EXAMPLE = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

EXAMPLE2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


@dataclasses.dataclass
class Module(abc.ABC):
    name: str
    destinations: list[str]

    def handle(self, modules: dict[str, Module], source: str, pulse: bool) -> bool | None:
        pass

    @classmethod
    def from_string(cls, s: str) -> Module:
        if s[0] == '%':
            c = FlipFlop
            s = s[1:]
        elif s[0] == '&':
            c = Conjunction
            s = s[1:]
        else:
            c = Broadcast
        return c(
            name=s.split(' -> ')[0],
            destinations=s.split(' -> ')[1].split(', '),
        )


@dataclasses.dataclass
class FlipFlop(Module):
    state: bool = False

    def handle(self, modules: dict[str, Module], source: str, pulse: bool) -> bool | None:
        if not pulse:
            self.state = not self.state
            return self.state
        else:
            return None


@dataclasses.dataclass
class Conjunction(Module):
    states: dict[str, bool] = dataclasses.field(default_factory=dict)

    def handle(self, modules: dict[str, Module], source: str, pulse: bool) -> bool | None:
        self.states[source] = pulse
        return not all(self.states.values())


@dataclasses.dataclass
class Broadcast(Module):

    def handle(self, modules: dict[str, Module], source: str, pulse: bool) -> bool | None:
        return pulse


def part1(input_data: str):
    modules: dict[str, Module] = {m.name: m for line in input_data.splitlines() if (m := Module.from_string(line))}
    modules['button'] = Broadcast('button', ['broadcaster'])
    counts = [0, 0]

    for m in modules.values():
        if isinstance(m, Conjunction):
            for n in modules.values():
                if m.name in n.destinations:
                    m.states[n.name] = False

    def cycle():
        signals = [('button', '', False)]
        while signals:
            name, prev_name, prev_signal = signals.pop(0)
            if name not in modules:
                continue
            module = modules[name]
            next_signal = module.handle(modules, prev_name, prev_signal)
            if next_signal is None:
                continue
            counts[next_signal] += len(module.destinations)
            for destination in module.destinations:
                # print(f'{name} -{"high" if next_signal else "low"}-> {destination}')
                signals.append((destination, name, next_signal))

    for i in range(1000):
        cycle()

    return counts[0] * counts[1]


def part2(input_data: str):
    pass


if __name__ == '__main__':
    assert part1(EXAMPLE) == 32000000
    assert part1(EXAMPLE2) == 11687500
    print(f'Solution for part 1 is: {part1(get_input())}')

    assert part2(EXAMPLE) == None
    print(f'Solution for part 2 is: {part2(get_input())}')
