from .base import Base
from .primitivetype import PRIMITIVE_TYPES, PrimitiveType

from . import helper


class DelegateParameter(Base):
    def __init__(self, name, delegate, type, api_name=None, required=True, default=None, documentation=None):
        Base.__init__(self, name, delegate)
        
        self.__required = required
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_method_parameter_api_name(self.identifier)
        
        self.__type = type
        self.__default = default
        
        self.__documentation = documentation
    
    @property
    def delegate(self):
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
    def default(self):
        return self.__default
    
    @property
    def documentation(self):
        return self.__documentation
    
    def __repr__(self):
        return "<Parameter %s of Delegate %s>"%(self.name, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[self.__type]
            
            if not self.__required:
                if self.__default is None:
                    self.__default = self.__type.default
                else:
                    self.__default = self.__type.convert(self.__default)
        elif self.__type != '*':
            self.__type = builder.get_type_by_name(self.__type)
            self.__default = None
