from .checkdata import check_any


class DiagramTemplate:
    def __init__(self, type, data, parent_id):
        self.__type = type
        self.__data = data
        self.__parent_id = parent_id
    
    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return self.__data
    
    @property
    def parent_id(self):
        return self.__parent_id

    def _compile(self, metamodel):
        self.__type = metamodel.get_diagram_type(self.__type)

        self.__data = check_any(self.__type.ufl_type, self.__data)
