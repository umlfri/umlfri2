class ProjectTemplate:
    def __init__(self, id, elements, connections, diagrams):
        self.__id = id
        self.__elements = elements
        self.__connections = connections
        self.__diagrams = diagrams
        self.__metamodel = None
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = metamodel
    
    @property
    def id(self):
        return self.__id
    
    @property
    def icon(self):
        return self.__metamodel.addon.icon
    
    @property
    def addon(self):
        return self.__metamodel.addon

    @property
    def metamodel(self):
        return self.__metamodel
    
    @property
    def elements(self):
        yield from self.__elements

    @property
    def connections(self):
        yield from self.__connections
    
    @property
    def diagrams(self):
        yield from self.__diagrams
    
    def compile(self):
        for element in self.__elements:
            element._compile(self.__metamodel)

        for connection in self.__connections:
            connection._compile(self.__metamodel)
        
        for diagram in self.__diagrams:
            diagram._compile(self.__metamodel)
