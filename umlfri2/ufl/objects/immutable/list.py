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
    
    def __eq__(self, other):
        if not isinstance(other, UflList):
            return NotImplemented
        
        if self.__type is not other.__type:
            return NotImplemented
        
        if self.get_length() != other.get_length():
            return False
        
        for mine, theirs in zip(self.__values, other.__values):
            if mine != theirs:
                return False
        
        return True
    
    def make_mutable(self):
        return UflMutableList(self.__type, self.__values)
    
    def apply_patch(self, patch):
        if not isinstance(patch, UflListPatch) or patch.type != self.__type:
            raise ValueError()
        
        to_add = []
        to_remove = []
        to_apply = []
        
        for change in patch:
            if isinstance(change, UflListPatch.ItemRemoved):
                to_remove.append(change.index)
            elif isinstance(change, UflListPatch.ItemMoved):
                to_remove.append(change.old_index)
                to_add.append((change.new_index, change.value))
            elif isinstance(change, UflListPatch.ItemAdded):
                to_add.append((change.index, change.new_value))
            if isinstance(change, UflListPatch.ItemPatch):
                to_apply.append((change.index, change.patch))
        
        to_add.sort()
        to_remove.sort()
        to_remove.reverse()
        
        for index in to_remove:
            del self.__values[index]
        
        for index, new_value in to_add:
            self.__values.insert(index, new_value)
        
        for index, inner_patch in to_apply:
            self.__values[index].apply_patch(inner_patch)
    
    def copy(self):
        if self.__type.item_type.is_immutable:
            return UflList(self.__type, self.__values)
        else:
            return UflList(self.__type, [value.copy() for value in self.__values])
