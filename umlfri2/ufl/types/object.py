from .type import UflType


class UflObjectType(UflType):
    def __init__(self, attributes):
        self.__attributes = list(attributes)
    
    @property
    def attributes(self):
        yield from self.__attributes
