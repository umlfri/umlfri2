from weakref import ref


class Metamodel:
    def __init__(self, diagrams, elements, connections):
        self.__diagrams = diagrams
        self.__elements = elements
        self.__connections = connections
        
        self.__addon = None
        self.__config_structure = None
    
    def _set_addon(self, addon):
        self.__addon = ref(addon)
        
        for diagram in self.__diagrams.values():
            diagram._set_metamodel(self)
        
        for element in self.__elements.values():
            element._set_metamodel(self)
        
        for connection in self.__connections.values():
            connection._set_metamodel(self)
    
    @property
    def addon(self):
        return self.__addon()
    
    def get_element_type(self, name):
        return self.__elements[name]
    
    def get_diagram_type(self, name):
        return self.__diagrams[name]
    
    def get_connection_type(self, name):
        return self.__connections[name]
    
    def compile(self):
        for diagram in self.__diagrams.values():
            diagram.compile()
        
        for element in self.__elements.values():
            element.compile()
        
        for connection in self.__connections.values():
            connection.compile()
