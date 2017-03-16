from collections import namedtuple
from enum import Enum, unique


@unique
class AddOnDependencyType(Enum):
    starter = 1
    interface = 2


AddOnDependency = namedtuple('Dependency', ('type', 'id'))
