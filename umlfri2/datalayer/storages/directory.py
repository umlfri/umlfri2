import os
import os.path
from .storage import Storage, StorageReference


class DirectoryStorageReference(StorageReference):
    def __init__(self, path, mode):
        self.__path = path
        self.__mode = mode
    
    @property
    def name(self):
        return self.__path
    
    def open(self, mode=None):
        if mode is None:
            mode = self.__mode
        return DirectoryStorage(self.__path, mode)


class DirectoryStorage(Storage):
    @staticmethod
    def read_storage(path):
        if os.path.isdir(path):
            return DirectoryStorage(os.path.abspath(path), 'r')
    
    def __init__(self, path, mode):
        self.__path = path
        self.__mode = mode
    
    def list(self, path=None):
        return os.listdir(self.__fix_path(path))

    def open(self, path, mode='r'):
        if mode != 'r' and self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        path = self.__fix_path(path)
        if mode == 'w':
            dir = os.path.dirname(path)
            if not os.path.exists(dir):
                os.makedirs(dir, exist_ok=True)
            return open(path, 'wb')
        else:
            if os.path.exists(path):
                return open(path, 'rb')
    
    def exists(self, path):
        path = self.__fix_path(path)
        return os.path.exists(path)
    
    def create_substorage(self, path):
        path = self.__fix_path(path)
        if os.path.exists(path):
            return Storage.read_storage(path)
    
    def get_all_files(self):
        for dirpath, dirs, files in os.walk(self.__path):
            for file in files:
                yield os.path.join(dirpath, file)
    
    def __fix_path(self, path):
        if path is None:
            return self.__path
        
        return os.path.join(self.__path, path)
    
    def remember_reference(self):
        return DirectoryStorageReference(self.__path, self.__mode)
    
    def close(self):
        pass
