from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType

from . import helper


class InterfaceMethodParameter(Base):
    def __init__(self, name, interface_method, type, api_name=None, required=True, nullable=False, default=None,
                 documentation=None):
        Base.__init__(self, name, interface_method)
        
        self.__required = required
        self.__nullable = nullable
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_method_parameter_api_name(self.identifier)
        
        if type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[type]
            
            if not self.__required:
                if default is None:
                    self.__default = None
                else:
                    self.__default = self.__type.convert(default)
            else:
                self.__default = None
        else:
            self.__type = type
            self.__default = None
        
        self.__documentation = documentation
    
    @property
    def interface_method(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def fqn(self):
        return self.parent.fqn + "(" + self.name + ")"
    
    @property
    def required(self):
        return self.__required
    
    @property
    def nullable(self):
        return self.__nullable
    
    @property
    def default(self):
        return self.__default
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        if self.__type != '*' and not isinstance(self.__type, PrimitiveType):
            yield self.__type
    
    def __repr__(self):
        return "<Parameter %s of InterfaceMethod %s>"%(self.name, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type != '*' and not isinstance(self.__type, PrimitiveType):
            self.__type = builder.get_type_by_name(self.__type)
