from enum import Enum, unique


@unique
class AddOnState(Enum):
    none = 1
    stopped = 2
    starting = 3
    started = 4
    stopping = 5
    error = 6
