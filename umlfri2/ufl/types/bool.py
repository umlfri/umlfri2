from .type import UflType


class UflBoolType(UflType):
    def __init__(self, default=False):
        self.__default = default
    
    @property
    def default(self):
        return self.__default
    
    def __str__(self):
        return 'Bool'