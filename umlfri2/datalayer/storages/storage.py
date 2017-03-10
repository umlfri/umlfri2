class StorageReference:
    @property
    def name(self):
        raise NotImplementedError
    
    def open(self, mode=None):
        raise NotImplementedError

class Storage:
    @staticmethod
    def read_storage(path):
        for subclass in Storage.__subclasses__():
            ret = subclass.read_storage(path)
            if ret is not None:
                return ret
        raise Exception("Storage {0} not found".format(path))
    
    def list(self, path=None):
        raise NotImplementedError
    
    def open(self, path, mode='r'):
        raise NotImplementedError
    
    def exists(self, path):
        raise NotImplementedError
    
    def create_substorage(self, path):
        raise NotImplementedError
    
    def make_dir(self, path):
        raise NotImplementedError
    
    def get_all_files(self):
        raise NotImplementedError
    
    def copy_from(self, storage):
        raise NotImplementedError
    
    def remember_reference(self):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
