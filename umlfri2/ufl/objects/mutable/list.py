from umlfri2.ufl.uniquevaluegenerator import UniqueValueGenerator
from .mutable import UflMutable
from ..patch import UflListPatch


class ListItemValueGenerator(UniqueValueGenerator):
    def __init__(self, list):
        self.__list = list
        self.__name = None
    
    def get_parent_name(self):
        return None
    
    def for_name(self, name):
        ret = ListItemValueGenerator(self.__list)
        ret.__name = name
        return ret
    
    def has_value(self, value):
        if self.__name is None:
            return None
        
        for item in self.__list:
            if item.get_value(self.__name) == value:
                return True
        
        return False


class UflMutableList(UflMutable):
    def __init__(self, type, values):
        if type.item_type.is_immutable:
            self.__values = list(enumerate(values))
        else:
            self.__values = list(enumerate(value.make_mutable() for value in values))
        
        self.__type = type
        self.__old_values = values[:]
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        for index, value in self.__values:
            yield value

    def __bool__(self):
        return bool(self.__values)
    
    def __eq__(self, other):
        if not isinstance(other, UflMutableList):
            return NotImplemented
        
        if self.__type is not other.__type:
            return NotImplemented
        
        if self.get_length() != other.get_length():
            return False
        
        for mine, theirs in zip(self.__values, other.__values):
            if mine != theirs:
                return False
        
        return True
    
    def get_item(self, index):
        return self.__values[index][1]
    
    def set_item(self, index, value):
        item_type = self.__type.item_type
        
        if item_type.is_immutable and not item_type.is_valid_value(value):
            raise ValueError
        self.__values[index] = None, value
    
    def get_length(self):
        return len(self.__values)
    
    def create_default(self):
        ret = self.__type.item_type.build_default(ListItemValueGenerator(self))
        if self.type.item_type.is_immutable:
            return ret
        else:
            return ret.make_mutable()
    
    def append(self, value=None):
        if value is None:
            value = self.create_default()
        elif not self.__type.item_type.is_valid_value(value):
            raise ValueError
        elif not self.__type.item_type.is_immutable:
            if not isinstance(value, UflMutable):
                value = value.make_mutable()
        self.__values.append((None, value))
        return value
    
    def delete(self, index):
        del self.__values[index]
    
    def make_immutable(self):
        from ..immutable import UflList
        
        if self.__type.item_type.is_immutable:
            values = [value for index, value in self.__values]
        else:
            values = [value.make_immutable() for index, value in self.__values]

        return UflList(self.__type, values)
    
    def make_patch(self):
        kept_indices = {index for index, value in self.__values}
        
        changes = []
        
        for index in reversed(range(len(self.__old_values))):
            if index not in kept_indices:
                changes.append(UflListPatch.ItemRemoved(index, self.__old_values[index]))
        
        for new_index, (index, value) in enumerate(self.__values):
            if index is None:
                if not self.__type.item_type.is_immutable:
                    value = value.make_immutable()
                
                changes.append(UflListPatch.ItemAdded(new_index, value))
            elif not self.__type.item_type.is_immutable:
                patch = value.make_patch()
                if patch.has_changes:
                    changes.append(UflListPatch.ItemPatch(new_index, patch))
        
        return UflListPatch(self.__type, changes)
    
    def copy(self):
        ret = UflMutableList(self.__type, [])
        if self.__type.item_type.is_immutable:
            ret.__values = self.__values[:]
        else:
            ret.__values = [(index, value.copy()) for index, value in self.__values]
        ret.__old_values = self.__old_values
        return ret
