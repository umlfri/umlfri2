from enum import Enum, unique


@unique
class VerticalAlignment(Enum):
    top = 1
    center = 2
    bottom = 3


@unique
class HorizontalAlignment(Enum):
    left = 1
    center = 2
    right = 3
