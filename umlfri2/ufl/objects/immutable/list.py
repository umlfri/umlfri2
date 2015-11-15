from umlfri2.ufl.objects.mutable import UflMutableList


class UflList:
    def __init__(self, type, values=None):
        if values is None:
            self.__values = []
        else:
            self.__values = values[:]
        self.__type = type
    
    @property
    def type(self):
        return self.__type
    
    def __iter__(self):
        yield from self.__values
    
    def get_item(self, index):
        return self.__values[index]
    
    def get_length(self):
        return len(self.__values)
    
    def __bool__(self):
        return bool(self.__values)
    
    def make_mutable(self):
        return UflMutableList(self.__type, self.__values)
