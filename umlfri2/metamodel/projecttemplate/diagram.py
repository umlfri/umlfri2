from .checkdata import check_any


class DiagramTemplate:
    def __init__(self, type, data, elements, connections, parent_id):
        self.__type = type
        self.__data = data
        self.__elements = elements
        self.__connections = connections
        self.__parent_id = parent_id
    
    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return self.__data
    
    @property
    def elements(self):
        yield from self.__elements
    
    @property
    def connections(self):
        yield from self.__connections
    
    @property
    def parent_id(self):
        return self.__parent_id

    def _compile(self, metamodel):
        self.__type = metamodel.get_diagram_type(self.__type)

        self.__data = check_any(self.__type.ufl_type, self.__data)
