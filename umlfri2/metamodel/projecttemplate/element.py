class ElementTemplate:
    def __init__(self, type, data, children, id=None):
        self.__id = id
        self.__type = type
        self.__data = data
        self.__children = children
    
    @property
    def id(self):
        return self.__id
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def children(self):
        yield from self.__children
    
    def _compile(self, metamodel):
        self.__type = metamodel.get_element_type(self.__type)
        
        for child in self.__children:
            child._compile(metamodel)
