from enum import Enum, unique


@unique
class Order(Enum):
    Asc = 1
    Desc = 2
