from .base import Base


class InterfacePropertyThrows(Base):
    def __init__(self, interface_property, exception, documentation=None):
        Base.__init__(self, None, interface_property)
        
        self.__exception = exception
        self.__documentation = documentation
    
    @property
    def interface_property(self):
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
    
    @property
    def referenced(self):
        yield self.__exception
    
    def __repr__(self):
        return "<Throws %s from InterfaceProperty %s>"%(self.exception.fqn, self.parent.fqn)
    
    def _link(self, builder):
        Base._link(self, builder)
        
        self.__exception = builder.get_type_by_name(self.__exception)
