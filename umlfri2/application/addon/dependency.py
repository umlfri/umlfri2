from enum import Enum, unique


@unique
class AddOnDependencyType(Enum):
    starter = 1
    interface = 2


class AddOnDependency:
    def __init__(self, type, id, version=None):
        self.__type = type
        self.__id = id
        self.__version = version
    
    @property
    def type(self):
        return self.__type
    
    @property
    def id(self):
        return self.__id
    
    @property
    def version(self):
        return self.__version
    
    def __hash__(self):
        return hash(self.__type) + hash(self.__id) * 293
    
    def __eq__(self, other):
        if not isinstance(other, AddOnDependency):
            return False
        
        return self.__version == other.__version and self.__type == other.__type
