from .type import UflType


class UflObjectType(UflType):
    def __init__(self, attributes):
        self.__attributes = dict(attributes)
    
    @property
    def attributes(self):
        return self.__attributes.copy()
    
    def get_attribute_type(self, name):
        return self.__attributes[name]
    
    def contains_attribute(self, name):
        return name in self.__attributes
