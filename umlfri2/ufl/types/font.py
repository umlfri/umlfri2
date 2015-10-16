from .umlfri2.ufl.structure.type import UflType


class UflFontType(UflType):
    def __init__(self, default=None):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
