from ..base.type import UflType


class UflGenericType(UflType):
    def __init__(self, base_type):
        self.__base_type = base_type
    
    def resolve_generic(self, actual_type, generics_cache):
        if self in generics_cache:
            if generics_cache[self].is_assignable_from(actual_type):
                return generics_cache[self]
            return None
        if self.__base_type.is_assignable_from(actual_type):
            generics_cache[self] = actual_type
            return actual_type
        return None
