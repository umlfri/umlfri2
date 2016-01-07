from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType


class DelegateThrows(Base):
    def __init__(self, interface_method, exception, documentation=None):
        Base.__init__(self, None, interface_method)
        
        self.__exception = exception
        self.__documentation = documentation
    
    @property
    def delegate(self):
        return self.parent
    
    @property
    def exception(self):
        return self.__exception
    
    @property
    def fqn(self):
        return self.parent.fqn + "::__throws__(" + self.exception.fqn + ")"
    
    @property
    def documentation(self):
        return self.__documentation
    
    def __repr__(self):
        return "<Throws %s from Delegate %s>"%(self.exception.fqn, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if not isinstance(self.__exception, PrimitiveType):
            self.__exception = builder.get_type_by_name(self.__exception)
