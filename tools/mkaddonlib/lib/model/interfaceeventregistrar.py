from .base import Base
from .interfacemethod import InterfaceMethod

from . import helper


class InterfaceEventRegistrar(Base):
    def __init__(self, interface_event, api_name=None):
        Base.__init__(self, None, interface_event)
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_event_registrar_api_name(self.identifier)
    
    @property
    def interface_event(self):
        return self.parent
    
    @property
    def name(self):
        return self.parent.name
    
    @property
    def singular(self):
        return self.parent.singular
    
    @property
    def type(self):
        return self.parent.type
    
    @property
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.fqn + '::' + '__register__'
    
    @property
    def api_name(self):
        return self.__api_name
    
    def create_method(self, name=None, handler='handler'):
        if name is None:
            name = self.name
        meth = InterfaceMethod(name, self.interface_event.interface, api_name=self.api_name, mutator=True,
                               transactional=False, async_execution=True, documentation=self.interface_event.documentation)
        
        return meth
    
    def __repr__(self):
        return "<Registrar of InterfaceEvent {0}>".format(self.parent.fqn)
