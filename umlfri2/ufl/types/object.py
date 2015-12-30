from .type import UflType
from ..objects import UflObject


class UflObjectAttribute:
    def __init__(self, name, type):
        self.__name = name
        self.__type = type
        self.__parent = None
    
    @property
    def name(self):
        return self.__name
    
    @property
    def type(self):
        return self.__type
    
    @property
    def parent(self):
        return self.__parent
    
    def set_parent(self, parent):
        if self.__parent is not None:
            raise Exception
        self.__parent = parent
        self.__type.set_parent(self)


class UflObjectType(UflType):
    def __init__(self, attributes):
        self.__attributes = attributes.copy()
    
    @property
    def attributes(self):
        yield from self.__attributes.values()
    
    @property
    def has_attributes(self):
        return len(self.__attributes) > 0
    
    def get_attribute(self, name):
        return self.__attributes[name]
    
    def contains_attribute(self, name):
        return name in self.__attributes
    
    def build_default(self, generator):
        ret = {}
        for attr in self.__attributes.values():
            local_generator = None
            if generator:
                local_generator = generator.for_name(attr.name)
            
            ret[attr.name] = attr.type.build_default(local_generator)
        
        return UflObject(self, ret)
    
    def is_same_as(self, other):
        if not super().is_same_as(other):
            return False
        
        if self.__attributes.keys() != other.__attributes.keys():
            return False
        
        for name, type in self.__attributes:
            if not other.__attributes[name].type.is_same_as(type):
                return False
        
        return True
    
    @property
    def is_immutable(self):
        return False
    
    def is_default_value(self, value):
        for attr in self.__attributes.values():
            if not attr.type.is_default_value(value.get_value(attr.name)):
                return False
        return True
    
    def set_parent(self, parent):
        super().set_parent(parent)
        for attr in self.__attributes.values():
            attr.set_parent(self)
    
    def __str__(self):
        return "Object[{0}]".format(", ".join("{0}: {1}".format(attr.name, attr.type) for attr in self.__attributes.values()))
