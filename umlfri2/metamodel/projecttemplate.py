class ProjectTemplate:
    def __init__(self, storage, name, path):
        self.__name = name
        self.__storage = storage
        self.__path = path
        self.__metamodel = None
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = metamodel
    
    @property
    def name(self):
        return self.__name
    
    @property
    def icon(self):
        return self.__metamodel.addon.icon
    
    @property
    def storage(self):
        return self.__storage
    
    @property
    def path(self):
        return self.__path
    
    @property
    def addon(self):
        return self.__metamodel.addon
    
    def load(self):
        return self.__storage.open(self.__path)
