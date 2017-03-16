from enum import Enum, unique


@unique
class ArrowOrientation(Enum):
    source = 1
    destination = 2
