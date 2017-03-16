from enum import Enum, unique


@unique
class LineOrientation(Enum):
    auto = 1
    horizontal = 2
    vertical = 3
