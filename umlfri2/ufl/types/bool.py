from .umlfri2.ufl.structure.type import UflType


class UflBoolType(UflType):
    def __init__(self, default=False):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
