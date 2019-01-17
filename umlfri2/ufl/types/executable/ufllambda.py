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
    
    def resolve_generic(self, actual_type, generics_cache):
        if not isinstance(actual_type, UflLambdaType):
            return None
        
        if len(self.__parameter_types) != len(actual_type.__parameter_types):
            return None
        
        resolved_return_type = self.__return_type.resolve_generic(actual_type.__return_type, generics_cache)
        if resolved_return_type is None:
            return None
        
        resolved_parameter_types = []
        for self_param, actual_param in zip(self.__parameter_types, actual_type.__parameter_types):
            resolved_parameter_type = self_param.resolve_generic(actual_param, generics_cache)
            if resolved_parameter_type is None:
                return None
            resolved_parameter_types.append(resolved_parameter_type)
        
        return UflLambdaType(resolved_parameter_types, resolved_return_type)
