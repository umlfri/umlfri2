from weakref import ref


class ElementType:
    def __init__(self, id, icon, ufl_type, display_name, appearance):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__display_name = display_name
        self.__appearance = appearance
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = ref(metamodel)
    
    @property
    def metamodel(self):
        return self.__metamodel
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def ufl_type(self):
        return self.__ufl_type
    
    def compile(self):
        variables = {'self': self.__ufl_type, 'cfg': self.__metamodel().addon.config_structure}
        
        self.__appearance.compile(variables)
        self.__display_name.compile(variables)
    
    def create_visual_object(self, context, ruler):
        context.set_config(self.__metamodel().addon.config)
        return self.__appearance.create_visual_object(context, ruler)
    
    def get_display_name(self, context):
        context.set_config(self.__metamodel().addon.config)
        return self.__display_name.get_text(context)
