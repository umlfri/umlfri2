from weakref import ref


class ConnectionType:
    def __init__(self, id, icon, ufl_type, appearance, labels):
        self.__metamodel = None
        self.__id = id
        self.__icon = icon
        self.__ufl_type = ufl_type
        self.__appearance = appearance
        self.__labels = {label.id: label for label in labels}
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = ref(metamodel)
        
        for label in self.__labels.values():
            label._set_connection_type(self)
    
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
    def labels(self):
        return self.__labels.values()
    
    def get_label(self, id):
        return self.__labels[id]
    
    def compile(self):
        variables = {'self': self.__ufl_type, 'cfg': self.__metamodel().addon.config_structure}
        
        self.__appearance.compile(variables)
        for label in self.__labels.values():
            label.compile()
    
    def create_appearance_object(self, context, ruler):
        context = context.extend(self.__metamodel().addon.config, 'cfg')
        return self.__appearance.create_connection_object(context)
