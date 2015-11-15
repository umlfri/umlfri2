from umlfri2.ufl.objects.mutable import UflMutableObject


class UflObject:
    def __init__(self, type, attributes):
        self.__type = type
        self.__attributes = attributes.copy()
    
    @property
    def type(self):
        return self.__type
    
    def get_values(self):
        yield from self.__attributes.items()
    
    def get_value(self, name):
        return self.__attributes[name]
    
    def make_mutable(self):
        return UflMutableObject(self.__type, self.__attributes)
