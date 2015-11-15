from ..patch import UflObjectPatch
from ..mutable import UflMutableObject


class UflObject:
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = attributes.copy()
    
    @property
    def type(self):
        return self.__type
    
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
