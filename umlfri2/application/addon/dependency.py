from collections import namedtuple


class AddOnDependencyType:
    starter = 0
    interface = 1


AddOnDependency = namedtuple('Dependency', ('type', 'id'))
