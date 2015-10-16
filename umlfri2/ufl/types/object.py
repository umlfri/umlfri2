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
    
    def build_default(self):
        return {name: type.build_default() for name, type in self.__attributes.items()}
    
    def __str__(self):
        return "Object[{0}]".format(", ".join("{0}: {1}".format(name, type) for name, type in self.__attributes.items()))
