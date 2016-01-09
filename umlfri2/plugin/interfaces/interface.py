class Interface:
    @property
    def id(self):
        raise NotImplementedError
    
    @property
    def type(self):
        return self.__class__.__name__[1:]
