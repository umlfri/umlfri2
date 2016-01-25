from .immutable import UflImmutable
from ..patch import UflObjectPatch
from ..mutable import UflMutableObject


class UflObject(UflImmutable):
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = attributes.copy()
    
    @property
    def type(self):
        return self.__type
    
    def __eq__(self, other):
        if not isinstance(other, UflObject):
            return NotImplemented
        
        if self.__type is not other.__type:
            return NotImplemented
        
        for name, mine in self.__attributes:
            theirs = other.__attributes[name]
            if mine != theirs:
                return False
        
        return True
    
    def get_values(self):
        yield from self.__attributes.items()
    
    def get_value(self, name):
        return self.__attributes[name]
    
    def make_mutable(self):
        return UflMutableObject(self.__type, self.__attributes)
    
    def apply_patch(self, patch):
        if not isinstance(patch, UflObjectPatch) or patch.type != self.__type:
            raise ValueError()
        
        for change in patch:
            if isinstance(change, UflObjectPatch.AttributeChanged):
                self.__attributes[change.name] = change.new_value
            elif isinstance(change, UflObjectPatch.AttributePatch):
                self.__attributes[change.name].apply_patch(change.patch)
    
    def copy(self):
        attributes = {}
        
        for name, value in self.__attributes.items():
            if self.__type.get_attribute(name).is_immutable:
                attributes[name] = value
            else:
                attributes[name] = value.copy()
        
        return UflObject(self.__type, attributes)
