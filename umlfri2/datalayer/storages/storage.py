class Storage:
    @staticmethod
    def create_storage(path, mode='r'):
        for subclass in Storage.__subclasses__():
            ret = subclass.create_storage(path, mode)
            if ret is not None:
                return ret
    
    def list(self, path=None):
        raise NotImplementedError
    
    def open(self, path, mode='r'):
        raise NotImplementedError
    
    def exists(self, path):
        raise NotImplementedError
    
    def create_substorage(self, path):
        raise NotImplementedError
    
    def get_all_files(self):
        raise NotImplementedError
