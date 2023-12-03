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

    def neighbours(self) -> list[Coordinate]:
        return [self.step(direction) for direction in Direction]


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
