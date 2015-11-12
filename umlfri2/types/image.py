class Image:
    def __init__(self, storage, path):
        self.__storage = storage
        self.__path = path
    
    @property
    def storage(self):
        return self.__storage
    
    @property
    def path(self):
        return self.__path
    
    def load(self):
        return self.__storage.read(self.__path)
    
    def __repr__(self):
        return "<Icon {0}>".format(self.__path)
