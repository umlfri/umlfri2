from .base import Base


class ExceptionStringifyProperty(Base):
    def __init__(self, exception_stringify, property):
        Base.__init__(self, None, exception_stringify)
        
        self.__property = property
    
    @property
    def exception(self):
        return self.parent.exception
    
    @property
    def exception_property(self):
        return self.__property
    
    def _link(self, builder):
        Base._link(self, builder)
        
        self.__property = self.parent.exception.get_child(self.__property)
