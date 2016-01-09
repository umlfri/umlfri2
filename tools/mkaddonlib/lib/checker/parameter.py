class UmlFriInterfaceMethodParameter:
    def __init__(self, name, type):
        self.__name = name
        self.__type = type
    
    @property
    def name(self):
        return self.__name
    
    @property
    def type(self):
        return self.__type
