from collections import namedtuple

FoundSignature = namedtuple('FoundSignature', ('self_type', 'parameter_types', 'return_type'))


class MacroSignature:
    def __init__(self, identifier, self_type, parameter_types, return_type):
        self.__identifier = identifier
        self.__self_type = self_type
        self.__parameter_types = tuple(parameter_types)
        self.__return_type = return_type
    
    def compare(self, selector, target_type, argument_types):
        if self.__identifier != selector:
            return None
        
        if not self.__self_type.is_assignable_from(target_type):
            return None
        
        if len(self.__parameter_types) != len(argument_types):
            return None
        
        for macro_parameter_type, call_parameter_type in zip(self.__parameter_types, argument_types):
            if not macro_parameter_type.is_assignable_from(call_parameter_type):
                return None
        
        return FoundSignature(self.__self_type, self.__parameter_types, self.__return_type)
