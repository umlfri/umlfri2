from .list import UflListType
from ..enum.flags import UflFlagsType
from ..base.type import UflType


class UflIterableType(UflType):
    def __init__(self, item_type):
        self.__item_type = item_type

    @property
    def item_type(self):
        return self.__item_type

    def is_assignable_from(self, other):
        if isinstance(other, (UflListType, UflFlagsType, UflIterableType)):
            return self.__item_type.is_assignable_from(other.item_type)
        else:
            return False
    
    def resolve_generic(self, actual_type, generics_cache):
        if not isinstance(actual_type, (UflListType, UflFlagsType, UflIterableType)):
            return None
        
        resolved_item_type = self.__item_type.resolve_generic(actual_type.item_type, generics_cache)
        if resolved_item_type is None:
            return None
        
        return UflIterableType(resolved_item_type)
    
    def __str__(self):
        return "Iterable<{0}>".format(self.__item_type)
