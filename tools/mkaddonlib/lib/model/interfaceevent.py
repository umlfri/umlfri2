from .basecontainer import BaseContainer
from .delegate import Delegate
from .interfaceeventregistrar import InterfaceEventRegistrar
from .interfaceeventderegistrar import InterfaceEventDeregistrar


class InterfaceEvent(BaseContainer):
    def __init__(self, name, interface, type, documentation=None):
        BaseContainer.__init__(self, name, interface)
        self.__type = type
        self.__documentation = documentation
    
    @property
    def interface(self):
        return self.parent
    
    @property
    def type(self):
        return self.__type
    
    @property
    def documentation(self):
        return self.__documentation
    
    @property
    def referenced(self):
        yield self.__type
    
    @property
    def registrar(self):
        for child in self.children:
            if isinstance(child, InterfaceEventRegistrar):
                return child
    
    @property
    def deregistrar(self):
        for child in self.children:
            if isinstance(child, InterfaceEventDeregistrar):
                return child
    
    def _link(self, builder):
        BaseContainer._link(self, builder)
        
        delegate = builder.get_type_by_name(self.__type)
        if not isinstance(delegate, Delegate):
            raise Exception
        
        self.__type = delegate
