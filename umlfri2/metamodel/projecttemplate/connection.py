from .checkdata import check_any


class ConnectionTemplate:
    def __init__(self, type, data, source_id, destination_id, id=None):
        self.__id = id
        self.__type = type
        self.__data = data
        self.__source_id = source_id
        self.__destination_id = destination_id
    
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
    def source_id(self):
        return self.__source_id
    
    @property
    def destination_id(self):
        return self.__destination_id
    
    def _compile(self, metamodel):
        self.__type = metamodel.get_connection_type(self.__type)
        
        self.__data = check_any(self.__type.ufl_type, self.__data)
