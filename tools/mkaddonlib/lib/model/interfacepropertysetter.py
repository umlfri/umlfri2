from .basecontainer import BaseContainer
from .interfacepropertythrows import InterfacePropertyThrows
from .interfacemethod import InterfaceMethod
from .interfacemethodparameter import InterfaceMethodParameter
from .interfacemethodthrows import InterfaceMethodThrows

from . import helper


class InterfacePropertySetter(BaseContainer):
    def __init__(self, interface_property, api_name=None, transactional=True):
        BaseContainer.__init__(self, None, interface_property)
        if api_name is not None:
            self.__api_name = api_name
        else:
            self.__api_name = helper.compute_property_setter_api_name(self.singular, self.identifier)
        self.__transactional = transactional
    
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
        return self.parent.fqn + '::' + '__set__'
    
    @property
    def api_name(self):
        return self.__api_name
    
    @property
    def transactional(self):
        return self.__transactional
    
    def create_method(self, name=None, value='value'):
        if name is None:
            name = self.name
        meth = InterfaceMethod(name, self.interface_property.interface, api_name=self.api_name, mutator=True,
                               transactional=self.__transactional, documentation=self.interface_property.documentation)
        
        if self.index is not None:
            InterfaceMethodParameter(self.index.name, meth, self.index.type, api_name=self.index.api_name,
                                     documentation=self.index.documentation)
        
        InterfaceMethodParameter(value, meth, self.type, api_name='value')
        
        for throw in self.throws:
            InterfaceMethodThrows(meth, throw.exception, throw.documentation)
        
        return meth
    
    def __repr__(self):
        return "<Setter of InterfaceProperty %s>"%(self.parent.fqn)
