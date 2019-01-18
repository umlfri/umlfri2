from collections import namedtuple

FoundSignature = namedtuple('FoundSignature', ('self_type', 'parameter_types', 'return_type',
                                               'true_argument_types', 'true_result_type'))


class MacroSignature:
    def __init__(self, identifier, self_type, parameter_types, return_type):
        self.__identifier = identifier
        self.__self_type = self_type
        self.__parameter_types = tuple(parameter_types)
        self.__return_type = return_type
    
    def compare(self, selector, argument_type_checker):
        if self.__identifier != selector:
            return None
        
        result = argument_type_checker.check_arguments(self.__self_type, self.__parameter_types, self.__return_type)
        if result is not None:
            return FoundSignature(
                self.__self_type, self.__parameter_types, self.__return_type,
                tuple(result.argument_types), result.result_type
            )
        return None
