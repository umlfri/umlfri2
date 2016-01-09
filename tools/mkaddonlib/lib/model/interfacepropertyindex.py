from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType

from . import helper


class InterfacePropertyIndex(Base):
    def __init__(self, name, interface_property, type, api_name=None, documentation=None):
        Base.__init__(self, name, interface_property)
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_property_index_api_name(self.identifier)
        
        self.__type = type
        
        self.__documentation = documentation
    
    @property
    def interface_property(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def fqn(self):
        return self.parent.fqn + "[" + self.name + "]"
    
    @property
    def documentation(self):
        return self.__documentation
    
    def __repr__(self):
        return "<Index %s of InterfaceProperty %s>"%(self.name, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[self.__type]
        else:
            self.__type = builder.get_type_by_name(self.__type)
