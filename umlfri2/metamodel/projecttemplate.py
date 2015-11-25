class ProjectTemplate:
    def __init__(self, storage_ref, name, path):
        self.__name = name
        self.__storage_ref = storage_ref
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
    def addon(self):
        return self.__metamodel.addon
    
    def load(self):
        return self.__storage_ref.open().open(self.__path)
