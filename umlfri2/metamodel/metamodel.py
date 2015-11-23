from weakref import ref


class Metamodel:
    def __init__(self, diagrams, elements, connections, templates):
        self.__diagrams = diagrams
        self.__elements = elements
        self.__connections = connections
        self.__templates = templates
        
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
        
        for template in self.__templates:
            template._set_metamodel(self)
    
    @property
    def addon(self):
        return self.__addon()
    
    @property
    def diagram_types(self):
        yield from self.__diagrams.values()
    
    @property
    def element_types(self):
        yield from self.__elements.values()
    
    @property
    def connection_types(self):
        yield from self.__connections.values()
    
    @property
    def templates(self):
        yield from self.__templates
    
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
