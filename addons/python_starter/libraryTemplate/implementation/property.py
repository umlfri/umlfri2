class ApiPropertyIndexer:
    def __init__(self, name, documentation, instance, getter, setter, iterator):
        self.__name__ = name
        self.__doc__ = documentation
        
        self.__instance = instance
        self.__getter = getter
        self.__setter = setter
        self.__iterator = iterator
    
    def __getitem__(self, index):
        return self.__getter(self.__instance, index)
    
    def __setitem__(self, index, value):
        if self.__setter is None:
            raise AttributeError("Read-only property")
        else:
            self.__setter(self.__instance, index, value)
    
    def __iter__(self):
        if self.__iterator is None:
            raise TypeError("Property not iterable")
        else:
            return iter(self.__iterator(self.__instance))


class ApiProperty:
    def __init__(self, name, has_index, documentation):
        self.__name__ = name
        self.__doc__ = documentation
        
        self.__has_index = has_index
        
        self.__getter = None
        self.__setter = None
        self.__iterator = None
    
    def getter(self, function):
        self.__getter = function
        return self
    
    def setter(self, function):
        self.__setter = function
        return self
    
    def iterator(self, function):
        self.__iterator = function
        return self
    
    def __get__(self, instance, owner):
        if instance is None:
            return property(doc=self.__doc__)
        
        if self.__has_index:
            return ApiPropertyIndexer(self.__name__, self.__doc__, instance, self.__getter, self.__setter, self.__iterator)
        elif self.__iterator is not None:
            return iter(self.__iterator(instance))
        else:
            return self.__getter(instance)
    
    def __set__(self, instance, value):
        if self.__has_index or self.__setter is None:
            raise AttributeError("Read-only property")
        else:
            self.__setter(instance, value)
