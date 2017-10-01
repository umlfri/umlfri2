import os.path


class ProjectTemplate:
    def __init__(self, storage_ref, path):
        self.__storage_ref = storage_ref
        self.__path = path
        self.__metamodel = None
    
    def _set_metamodel(self, metamodel):
        self.__metamodel = metamodel
    
    @property
    def file_name(self):
        return os.path.basename(self.__path)
    
    @property
    def icon(self):
        return self.__metamodel.addon.icon
    
    @property
    def addon(self):
        return self.__metamodel.addon

    @property
    def metamodel(self):
        return self.__metamodel
    
    def load(self):
        return self.__storage_ref.open().open(self.__path)
