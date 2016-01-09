from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType


class InterfaceMethodReturn(Base):
    def __init__(self, interface_method, type, nullable=False, iterable=False, documentation=None):
        Base.__init__(self, None, interface_method)
        
        self.__iterable = iterable
        self.__nullable = nullable
        
        self.__type = type
        
        self.__documentation = documentation
    
    @property
    def interface_method(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def fqn(self):
        return self.parent.fqn + "::__return__"
    
    @property
    def nullable(self):
        return self.__nullable
    
    @property
    def iterable(self):
        return self.__iterable
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        if not isinstance(self.__type, PrimitiveType):
            yield self.__type
    
    def __repr__(self):
        return "<ReturnType of InterfaceMethod %s>"%(self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[self.__type]
        else:
            self.__type = builder.get_type_by_name(self.__type)
