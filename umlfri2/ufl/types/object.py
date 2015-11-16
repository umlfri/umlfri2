from .type import UflType
from ..objects import UflObject


class UflObjectType(UflType):
    def __init__(self, attributes):
        self.__attributes = attributes.copy()
    
    @property
    def attributes(self):
        yield from self.__attributes.items()
    
    def get_attribute_type(self, name):
        return self.__attributes[name]
    
    def contains_attribute(self, name):
        return name in self.__attributes
    
    def build_default(self, generator):
        attr = {}
        for name, type in self.__attributes.items():
            local_generator = None
            if generator:
                local_generator = generator.for_name(name)
            
            attr[name] = type.build_default(local_generator)
        
        return UflObject(self, attr)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        if self.__attributes.keys() != other.__attributes.keys():
            return False
        
        for name, type in self.__attributes:
            if not other.__attributes[name].is_same_as(type):
                return False
        
        return True
    
    @property
    def is_immutable(self):
        return False
    
    def __str__(self):
        return "Object[{0}]".format(", ".join("{0}: {1}".format(name, type) for name, type in self.__attributes.items()))
