import os
import os.path
from .storage import Storage


class DirectoryStorage(Storage):
    @staticmethod
    def open(path):
        if os.path.isdir(path):
            return DirectoryStorage(os.path.abspath(path))
    
    def __init__(self, path):
        self.__path = path
    
    def list(self, path):
        return os.listdir(self.__fix_path(path))

    def read(self, path):
        path = self.__fix_path(path)
        if os.path.exists(path):
            return open(path, 'rb')
    
    def exists(self, path):
        path = self.__fix_path(path)
        return os.path.exists(path)
    
    def sub_open(self, path):
        path = self.__fix_path(path)
        if os.path.exists(path):
            return Storage.open(path)
    
    def get_all_files(self):
        for dirpath, dirs, files in os.walk(self.__path):
            for file in files:
                yield os.path.join(dirpath, file)
    
    def __fix_path(self, path):
        return os.path.join(self.__path, path)
