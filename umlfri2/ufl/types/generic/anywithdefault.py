from ..base.type import UflType


class UflAnyWithDefault(UflType):
    def is_assignable_from(self, other):
        return other.has_default
    
    def resolve_unknown_generic(self, generics_cache):
        return None
    
    def resolve_generic(self, actual_type, generics_cache):
        if not actual_type.has_default:
            return None
        return actual_type
    
    def __str__(self):
        return 'AnyEquatable'
