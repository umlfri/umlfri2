class Storage:
    @staticmethod
    def open(path):
        for subclass in Storage.__subclasses__():
            ret = subclass.open(path)
            if ret is not None:
                return ret
    
    def list(self, path=None):
        raise NotImplementedError
    
    def read(self, path):
        raise NotImplementedError
    
    def exists(self, path):
        raise NotImplementedError
    
    def sub_open(self, path):
        raise NotImplementedError
    
    def get_all_files(self):
        raise NotImplementedError
