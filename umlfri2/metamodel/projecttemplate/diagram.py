from enum import Enum, unique

from .checkdata import check_any


@unique
class DiagramTemplateState(Enum):
    closed = 1
    opened = 2
    locked = 3


class DiagramTemplate:
    def __init__(self, type, data, elements, connections, parent_id, state=DiagramTemplateState.closed):
        self.__type = type
        self.__data = data
        self.__elements = elements
        self.__connections = connections
        self.__parent_id = parent_id
        self.__state = state
    
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
    
    @property
    def state(self):
        return self.__state

    def _compile(self, metamodel):
        self.__type = metamodel.get_diagram_type(self.__type)

        self.__data = check_any(self.__type.ufl_type, self.__data)
