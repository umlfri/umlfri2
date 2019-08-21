from ..base.type import UflType


class UflAnyComparableType(UflType):
    def is_assignable_from(self, other):
        return other.is_comparable_with(other)
    
    def resolve_unknown_generic(self, generics_cache):
        return None
    
    def resolve_generic(self, actual_type, generics_cache):
        if not actual_type.is_comparable_with(actual_type):
            return None
        return actual_type
    
    def __str__(self):
        return 'AnyEquatable'
