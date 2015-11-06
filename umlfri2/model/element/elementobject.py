from weakref import ref
from umlfri2.components.base.context import Context
from ..connection.connectionobject import ConnectionObject


class ElementObject:
    def __init__(self, parent, type):
        self.__parent = ref(parent)
        self.__type = type
        self.__data = type.ufl_type.build_default()
        self.__connections = []
        self.__children = []
        self.__diagrams = []
    
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
    
    @property
    def project(self):
        if isinstance(self.__parent, ElementObject):
            return self.__parent.__parent
        else:
            return self.__parent
    
    @property
    def children(self):
        yield from self.__children
    
    @property
    def diagrams(self):
        yield from self.__diagrams
    
    def create_child_element(self, type):
        obj = ElementObject(self, type)
        self.__children.append(obj)
        return obj
    
    def create_child_diagram(self, type):
        from ..diagram import Diagram # circular imports
        
        diagram = Diagram(self, type)
        self.__diagrams.append(diagram)
        return diagram
