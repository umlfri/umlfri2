from ..base.type import UflType


class UflAnyType(UflType):
    def is_assignable_from(self, other):
        return True
    
    def resolve_generic(self, actual_type, generics_cache):
        return actual_type
    
    def __str__(self):
        return 'Any'
