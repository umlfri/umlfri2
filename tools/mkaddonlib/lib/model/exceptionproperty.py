from .base import Base
from .primitivetype import PRIMITIVE_TYPES

from . import helper


class ExceptionProperty(Base):
    def __init__(self, name, exception, type, api_name=None, iterable=False, documentation=None):
        Base.__init__(self, name, exception)
        self.__documentation = documentation
        self.__iterable = iterable
        
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_exception_property_api_name(self.identifier)
        
        self.__type = type
    
    @property
    def exception(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def iterable(self):
        return self.__iterable
    
    @property
    def documentation(self):
        return self.__documentation
    
    def _link(self, builder):
        Base._link(self, builder)
        
        if self.__type in PRIMITIVE_TYPES:
            self.__type = PRIMITIVE_TYPES[self.__type]
        else:
            self.__type = builder.get_type_by_name(self.__type)
