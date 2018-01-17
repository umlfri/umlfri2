from weakref import ref

from umlfri2.ufl.context import Context


class ConnectionTypeLabel:
    def __init__(self, position, id, appearance):
        self.__connection_type = None
        self.__position = position
        self.__id = id
        self.__appearance = appearance
    
    def _set_connection_type(self, connection_type):
        self.__connection_type = ref(connection_type)
    
    @property
    def connection_type(self):
        return self.__connection_type()
    
    @property
    def position(self):
        return self.__position
    
    @property
    def id(self):
        return self.__id
    
    def compile(self, type_context):
        self.__appearance.compile(type_context)
    
    def create_appearance_object(self, connection, ruler):
        context = Context()\
            .set_variable('self', connection.data)\
            .set_variable('cfg', self.__connection_type().metamodel.config)
        return self.__appearance.create_visual_object(context, ruler)
