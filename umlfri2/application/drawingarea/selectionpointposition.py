from enum import Enum, unique


@unique
class SelectionPointPosition(Enum):
    first = 1
    center = 2
    last = 3