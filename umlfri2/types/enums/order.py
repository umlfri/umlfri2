from enum import Enum, unique


@unique
class Order(Enum):
    asc = 1
    desc = 2
