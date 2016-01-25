from .immutable import UflImmutable
from ..mutable import UflMutableFlags
from ..patch import UflFlagsPatch


class UflFlags(UflImmutable):
    def __init__(self, type, values=None):
        if values is None:
            self.__values = set()
        else:
            self.__values = values.copy()
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        for possibility in self.__type.possibilities:
            if possibility.value in self.__values:
                yield possibility.value
    
    def __contains__(self, item):
        return item in self.__values
    
    def __bool__(self):
        return bool(self.__values)
    
    def __eq__(self, other):
        if not isinstance(other, UflFlags):
            return NotImplemented
        
        if self.__type is not other.__type:
            return NotImplemented
        
        return self.__values == other.__values
    
    def make_mutable(self):
        return UflMutableFlags(self.__type, self.__values)
    
    def apply_patch(self, patch):
        if not isinstance(patch, UflFlagsPatch) or patch.type != self.__type:
            raise ValueError()
        
        for change in patch:
            if isinstance(change, UflFlagsPatch.ItemAdded):
                self.__values.add(change.new_value)
            elif isinstance(change, UflFlagsPatch.ItemRemoved):
                self.__values.remove(change.old_value)
    
    def copy(self):
        return UflFlags(self.__type, self.__values)
