class ProjectTemplate:
    def __init__(self, id, elements):
        self.__id = id
        self.__elements = elements
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
        return self.__elements
    
    def compile(self):
        for element in self.__elements:
            element._compile(self.__metamodel)
