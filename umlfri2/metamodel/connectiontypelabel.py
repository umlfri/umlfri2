from weakref import ref


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
    
    def compile(self):
        variables = {
            'self': self.__connection_type().ufl_type,
            'cfg': self.__connection_type().metamodel.addon.config_structure
        }
        
        self.__appearance.compile(variables)
    
    def create_appearance_object(self, context, ruler):
        context = context.extend(self.__connection_type().metamodel.addon.config, 'cfg')
        return self.__appearance.create_visual_object(context, ruler)
