class ElementType:
    def __init__(self, metamodel, id, icon, ufl_type, display_name, appearance):
        self.__metamodel = metamodel
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__display_name = display_name
        self.__appearance = appearance
    
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
    
    @property
    def display_name(self):
        return self.__display_name
    
    @property
    def appearance(self):
        return self.__appearance
    
    def compile(self):
        self.__appearance.compile({'self': self.__ufl_type, 'cfg': self.__metamodel.config_structure})
        self.__display_name.compile({'self': self.__ufl_type, 'cfg': self.__metamodel.config_structure})
    
    def create_visual_object(self, context, ruler):
        return self.__appearance.create_visual_object(context, ruler)
