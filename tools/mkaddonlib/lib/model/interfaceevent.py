from .base import Base
from .delegate import Delegate

from . import helper


class InterfaceEvent(Base):
    def __init__(self, name, interface, api_name, type, documentation=None):
        Base.__init__(self, name, interface)
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_event_api_name(self.identifier)
        self.__type = type
        self.__documentation = documentation
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def type(self):
        return self.__type
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        yield self.__type
    
    def _link(self, builder):
        Base._link(self, builder)
        
        delegate = builder.get_type_by_name(self.__type)
        if not isinstance(delegate, Delegate):
            raise Exception
        
        self.__type = delegate
