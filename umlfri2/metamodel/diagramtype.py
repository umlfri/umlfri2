from umlfri2.ufl.context import Context
from weakref import ref

from umlfri2.ufl.types import UflColorType


class DiagramType:
    def __init__(self, id, icon, ufl_type, display_name,
                 element_types, connection_types, background_color):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__ufl_type.set_parent(self)
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
    
    def get_background_color(self, diagram):
        context = Context()\
            .set_variable('self', diagram.data)\
            .set_variable('cfg', diagram.project.config)
        return self.__background_color(context)
    
    def compile(self, type_context):
        type_context = type_context \
            .set_variable_type('self', self.__ufl_type) \
            .set_variable_type('cfg', self.__metamodel().config_structure)
        
        self.__display_name.compile(type_context)
        self.__background_color.compile(type_context, UflColorType())
    
    def get_display_name(self, diagram):
        context = Context()\
            .set_variable('self', diagram.data)\
            .set_variable('cfg', diagram.project.config)
        return self.__display_name.get_text(context)
