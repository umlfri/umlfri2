from enum import Enum, unique


@unique
class LineStyle(Enum):
    solid = 1
    dot = 2
    dashdot = 3
