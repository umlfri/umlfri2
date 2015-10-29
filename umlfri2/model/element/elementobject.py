from umlfri2.components.base.context import Context
from ..connection.connectionobject import ConnectionObject


class ElementObject:
    def __init__(self, type):
        self.__type = type
        self.__data = type.ufl_type.build_default()
        self.__connections = []
    
    @property
    def type(self):
        return self.__type
    
    @property
    def data(self):
        return self.__data
    
    @property
    def connections(self):
        yield from self.__connections
    
    def get_display_name(self):
        context = Context(self.__data)
        return self.__type.get_display_name(context)
    
    def create_appearance_object(self, ruler):
        context = Context(self.__data)
        return self.__type.create_appearance_object(context, ruler)
    
    def connect_with(self, connection_type, second_element):
        connection = ConnectionObject(connection_type, self, second_element)
        self.__connections.append(connection)
        second_element.__connections.append(connection)
        return connection
