from .base import Base


class ExceptionStringifyText(Base):
    def __init__(self, exception_stringify, text):
        Base.__init__(self, None, exception_stringify)
        
        self.__text = text
    
    @property
    def exception(self):
        return self.parent.exception
    
    @property
    def text(self):
        return self.__text
