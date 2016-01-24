class UflEnumPossibility:
    def __init__(self, enum, name, value):
        self.__enum = enum
        self.__name = name
        self.__value = value
    
    @property
    def enum(self):
        return self.__enum
    
    @property
    def name(self):
        return self.__name
    
    @property
    def value(self):
        return self.__value