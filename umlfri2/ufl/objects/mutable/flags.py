from .mutable import UflMutable
from ..patch import UflFlagsPatch


class UflMutableFlags(UflMutable):
    def __init__(self, type, values):
        self.__values = values.copy()
        self.__type = type
        self.__old_values = values
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        for possibility in self.__type.possibilities:
            if possibility.value in self.__values:
                yield possibility.value
    
    def __contains__(self, item):
        return item in self.__values
    
    def set(self, value):
        if not self.__type.is_valid_possibility(value):
            raise ValueError
        
        self.__values.add(value)
    
    def unset(self, value):
        self.__values.remove(value)
    
    def get_length(self):
        return len(self.__values)
    
    def make_immutable(self):
        from ..immutable import UflFlags

        return UflFlags(self.__type, self.__values)
    
    def make_patch(self):
        changes = []
        
        for possibility in self.__type.possibilities:
            if possibility.value in self.__values and possibility.value not in self.__old_values:
                changes.append(UflFlagsPatch.ItemAdded(possibility.value))
            elif possibility.value not in self.__values and possibility.value in self.__old_values:
                changes.append(UflFlagsPatch.ItemRemoved(possibility.value))
        
        return UflFlagsPatch(self.__type, changes)
    
    def discard_changes(self):
        self.__values = self.__old_values.copy()
