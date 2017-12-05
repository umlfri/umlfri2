from .node import UflNode


class UflIteratorAccess(UflNode):
    def __init__(self, target, selector, parameters):
        self.__target = target
        self.__selector = selector
        self.__parameters = parameters

    @property
    def target(self):
        return self.__target

    @property
    def selector(self):
        return self.__selector

    @property
    def parameters(self):
        return self.__parameters

    def _get_params(self):
        return (self.__target, self.__selector) + tuple(self.__parameters)

    def accept(self, visitor):
        return visitor.visit_iterator_access(self)
