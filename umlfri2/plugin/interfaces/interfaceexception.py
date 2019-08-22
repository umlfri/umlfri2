class InterfaceException(Exception):
    def __init__(self, data):
        self.__data = data
    
    @property
    def type(self):
        return self.__class__.__name__
    
    @property
    def data(self):
        return self.__data
    
    def __str__(self):
        return "Public exception with data " + repr(self.__data)
