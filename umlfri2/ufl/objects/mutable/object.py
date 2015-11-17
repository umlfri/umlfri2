from .muttable import UflMutable
from umlfri2.ufl.objects.patch import UflObjectPatch


class UflMutableObject(UflMutable):
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = {}
        for name, value in attributes.items():
            if self.__type.get_attribute_type(name).is_immutable:
                new_value = value
            else:
                new_value = value.make_mutable()
            self.__attributes[name] = [value, new_value]
    
    @property
    def type(self):
        return self.__type
    
    def get_values(self):
        for name, (old_value, value) in self.__attributes.items():
            yield name, value
    
    def get_value(self, name):
        return self.__attributes[name][1]
    
    def set_value(self, name, value):
        attribute_type = self.__type.get_attribute_type(name)
        
        if attribute_type.is_immutable and  not attribute_type.is_valid_value(value):
            raise ValueError
        
        self.__attributes[name][1] = value
    
    def make_immutable(self):
        from ..immutable import UflObject
        
        attributes = {}
        for name, (old_value, value) in self.__attributes.items():
            if not self.__type.get_attribute_type(name).is_immutable:
                value = value.make_immutable()
            attributes[name] = value

        return UflObject(self.__type, attributes)
    
    def make_patch(self):
        changes = []
        for name, (old_value, value) in self.__attributes.items():
            if self.__type.get_attribute_type(name).is_immutable:
                if old_value is not value:
                    changes.append(UflObjectPatch.AttributeChanged(name, old_value, value))
            else:
                patch = value.make_patch()
                if patch.has_changes():
                    changes.append(UflObjectPatch.AttributePatch(name, patch))
        
        return UflObjectPatch(self.__type, changes)
