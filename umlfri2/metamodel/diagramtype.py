from umlfri2.types.color import Color
from weakref import ref


class DiagramType:
    def __init__(self, id, icon, ufl_type, display_name,
                 element_types, connection_types, background_color):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__display_name = display_name
        self.__element_types = tuple(element_types)
        self.__connection_types = tuple(connection_types)
        self.__background_color = background_color
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = ref(metamodel)
    
    @property
    def metamodel(self):
        return self.__metamodel()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def ufl_type(self):
        return self.__ufl_type
    
    @property
    def element_types(self):
        return self.__element_types
    
    @property
    def connection_types(self):
        return self.__connection_types
    
    def get_background_color(self, context):
        context = context.extend(self.__metamodel().addon.config, 'cfg')
        return self.__background_color(context)
    
    def compile(self):
        variables = {'self': self.__ufl_type, 'cfg': self.__metamodel().addon.config_structure}
        
        self.__display_name.compile(variables)
        self.__background_color.compile(variables, Color)
    
    def get_display_name(self, context):
        context = context.extend(self.__metamodel().addon.config, 'cfg')
        return self.__display_name.get_text(context)
