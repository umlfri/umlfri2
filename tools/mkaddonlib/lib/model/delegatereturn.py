from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType


class DelegateReturn(Base):
    def __init__(self, delegate, type, iterable=False, documentation=None):
        Base.__init__(self, None, delegate)
        
        self.__iterable = iterable
        
        if type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[type]
        else:
            self.__type = type
        
        self.__documentation = documentation
    
    @property
    def delegate(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def fqn(self):
        return self.parent.fqn + "::__return__"
    
    @property
    def iterable(self):
        return self.__iterable
    
    @property
    def documentation(self):
        return self.__documentation
    
    def __repr__(self):
        return "<ReturnType of Delegate %s>"%(self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__type, PrimitiveType):
            self.__type = builder.get_type_by_name(self.__type)
