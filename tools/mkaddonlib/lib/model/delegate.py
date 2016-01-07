from .basecontainer import BaseContainer
from .delegateparameter import DelegateParameter
from .delegatereturn import DelegateReturn


class Delegate(BaseContainer):
    def __init__(self, name, namespace, documentation=None):
        BaseContainer.__init__(self, name, namespace, sorted=False)
        self.__documentation = documentation
    
    @property
    def namespace(self):
        return self.parent
    
    @property
    def parameters(self):
        for child in self.children:
            if isinstance(child, DelegateParameter):
                yield child
    
    @property
    def return_type(self):
        for child in self.children:
            if isinstance(child, DelegateReturn):
                return child
    
    @property
    def documentation(self):
        return self.__documentation
