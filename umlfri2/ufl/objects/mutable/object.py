from .mutable import UflMutable
from umlfri2.ufl.objects.patch import UflObjectPatch


class UflMutableObject(UflMutable):
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = {}
        for name, value in attributes.items():
            if value is None:
                new_value = None
            elif self.__type.get_attribute(name).type.is_immutable:
                new_value = value
            else:
                new_value = value.make_mutable()
            self.__attributes[name] = [value, new_value]
    
    @property
    def type(self):
        return self.__type
    
    def __eq__(self, other):
        if not isinstance(other, UflMutableObject):
            return NotImplemented
        
        if self.__type is not other.__type:
            return NotImplemented
        
        for name, mine in self.__attributes.items():
            theirs = other.__attributes[name]
            if mine != theirs:
                return False
        
        return True
    
    def get_values(self):
        for name, (old_value, value) in self.__attributes.items():
            yield name, value
    
    def get_value(self, name):
        return self.__attributes[name][1]
    
    def set_value(self, name, value):
        attribute_type = self.__type.get_attribute(name).type
        
        if attribute_type.is_immutable:
            if not attribute_type.is_valid_value(value):
                raise ValueError
        else:
            if value.type is not attribute_type:
                raise ValueError
        
        self.__attributes[name][1] = value
    
    def make_immutable(self):
        from ..immutable import UflObject
        
        attributes = {}
        for name, (old_value, value) in self.__attributes.items():
            if not self.__type.get_attribute(name).type.is_immutable:
                value = value.make_immutable()
            attributes[name] = value

        return UflObject(self.__type, attributes)
    
    def make_patch(self):
        changes = []
        for name, (old_value, value) in self.__attributes.items():
            if self.__type.get_attribute(name).type.is_immutable:
                if old_value != value:
                    changes.append(UflObjectPatch.AttributeChanged(name, old_value, value))
            else:
                patch = value.make_patch()
                if patch.has_changes:
                    changes.append(UflObjectPatch.AttributePatch(name, patch))
        
        return UflObjectPatch(self.__type, changes)
    
    def copy(self):
        attributes = {}
        
        for name, (old_value, new_value) in self.__attributes.items():
            if self.__type.get_attribute(name).type.is_immutable:
                attributes[name] = [old_value, new_value]
            else:
                attributes[name] = [old_value, new_value.copy()]
        
        ret = UflMutableObject(self.__type, {})
        ret.__attributes = attributes
        
        return ret
