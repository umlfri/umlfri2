from ..base.type import UflType


class UflLambdaType(UflType):
    def __init__(self, parameter_types, return_type):
        self.__parameter_types = tuple(parameter_types)
        self.__return_type = return_type
    
    @property
    def parameter_count(self):
        return len(self.__parameter_types)
    
    @property
    def parameter_types(self):
        yield from self.__parameter_types
    
    @property
    def return_type(self):
        return self.__return_type
