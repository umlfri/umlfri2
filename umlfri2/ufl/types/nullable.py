from .type import UflType


class UflNullableType(UflType):
    def __init__(self, inner_type):
        self.__inner_type = inner_type
    
    @property
    def inner_type(self):
        return self.__inner_type
    
    def __str__(self):
        return "Nullable[{0}]".format(self.__inner_type)
