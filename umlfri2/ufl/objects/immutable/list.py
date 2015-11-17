from .immutable import UflImmutable
from ..mutable import UflMutableList
from ..patch import UflListPatch


class UflList(UflImmutable):
    def __init__(self, type, values=None):
        if values is None:
            self.__values = []
        else:
            self.__values = values[:]
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        yield from self.__values
    
    def get_item(self, index):
        return self.__values[index]
    
    def get_length(self):
        return len(self.__values)
    
    def __bool__(self):
        return bool(self.__values)
    
    def make_mutable(self):
        return UflMutableList(self.__type, self.__values)
    
    def apply_patch(self, patch):
        if not isinstance(patch, UflListPatch) or patch.type != self.__type:
            raise ValueError()
        
        for change in patch:
            if isinstance(change, UflListPatch.ItemAdded):
                self.__values.insert(change.index, change.new_value)
            elif isinstance(change, UflListPatch.ItemRemoved):
                del self.__values[change.index]
            elif isinstance(change, UflListPatch.ItemPatch):
                self.__values[change.index].apply_patch(change.patch)
