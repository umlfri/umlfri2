from .basecontainer import BaseContainer
from .interfacepropertythrows import InterfacePropertyThrows
from .interfacemethod import InterfaceMethod
from .interfacemethodreturn import InterfaceMethodReturn
from .interfacemethodthrows import InterfaceMethodThrows

from . import helper


class InterfacePropertyIterator(BaseContainer):
    def __init__(self, interface_property, api_name=None):
        BaseContainer.__init__(self, None, interface_property)
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_property_iterator_api_name(self.singular, self.identifier)
    
    @property
    def interface_property(self):
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
    def throws(self):
        for child in self.children:
            if isinstance(child, InterfacePropertyThrows):
                yield child
    
    @property
    def index(self):
        return self.parent.index
    
    @property
    def identifier(self):
        return self.parent.identifier
    
    @property
    def fqn(self):
        return self.parent.fqn + '::' + '__iter__'
    
    @property
    def api_name(self):
        return self.__api_name
    
    def create_method(self, name=None):
        if name is None:
            name = self.name
        meth = InterfaceMethod(name, self.interface_property.interface, api_name=self.api_name,
                               documentation=self.interface_property.documentation)
        
        ret = InterfaceMethodReturn(meth, self.type, iterable = True)
        meth.add_child(ret)
        
        for throw in self.throws:
            throws = InterfaceMethodThrows(meth, throw.exception, throw.documentation)
            meth.add_child(throws)
        
        return meth
    
    def __repr__(self):
        return "<Iterator of InterfaceProperty %s>"%(self.parent.fqn)
