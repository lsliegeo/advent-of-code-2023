from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Any


class Direction(Enum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'
    NORTH_WEST = 'north_west'
    NORTH_EAST = 'north_east'
    SOUTH_EAST = 'south_east'
    SOUTH_WEST = 'south_west'

    @staticmethod
    def orthogonal_directions() -> list[Direction]:
        return [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ]

    @staticmethod
    def opposite(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
            Direction.NORTH_EAST: Direction.SOUTH_WEST,
            Direction.SOUTH_WEST: Direction.NORTH_EAST,
            Direction.NORTH_WEST: Direction.SOUTH_EAST,
            Direction.SOUTH_EAST: Direction.NORTH_WEST,
        }[direction]


@dataclasses.dataclass(frozen=True)
class Coordinate:
    """
    Origin is upper left corner.

    +------->
    |      (y)
    |
    |
    v (x)
    """
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def step(self, direction: Direction):
        assert isinstance(direction, Direction)
        match direction:
            case Direction.NORTH | Direction.NORTH_EAST | Direction.NORTH_WEST:
                x_diff = -1
            case Direction.SOUTH | Direction.SOUTH_EAST | Direction.SOUTH_WEST:
                x_diff = 1
            case _:
                x_diff = 0
        match direction:
            case Direction.EAST | Direction.NORTH_EAST | Direction.SOUTH_EAST:
                y_diff = 1
            case Direction.WEST | Direction.NORTH_WEST | Direction.SOUTH_WEST:
                y_diff = -1
            case _:
                y_diff = 0
        return Coordinate(self.x + x_diff, self.y + y_diff)

    def neighbours(self, diagonal: bool) -> dict[Direction, Coordinate]:
        directions = list(Direction) if diagonal else Direction.orthogonal_directions()
        return {direction: self.step(direction) for direction in directions}


@dataclasses.dataclass
class Grid:
    """
    Origin is upper left corner.

    +------->
    |      (y)
    |
    |
    v (x)
    """
    items: dict[Coordinate, Any] = dataclasses.field(default_factory=dict)

    def visualize(self, filler: str = '.'):
        x_min, x_max = min(co.x for co in self.items), max(co.x for co in self.items)
        y_min, y_max = min(co.y for co in self.items), max(co.y for co in self.items)
        string = ''
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                value = self.items.get(Coordinate(x, y), filler)
                if isinstance(value, Enum):
                    value = value.value
                string += value
            string += '\n'
        print(string)

    @property
    def max_x(self) -> int:
        return max(co.x for co in self.items)

    @property
    def max_y(self) -> int:
        return max(co.y for co in self.items)
