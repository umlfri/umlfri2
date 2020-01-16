import os
import os.path

import shutil

from .storage import Storage, StorageReference


class DirectoryStorageReference(StorageReference):
    def __init__(self, path, mode):
        self.__path = path
        self.__mode = mode
    
    @property
    def name(self):
        return self.__path
    
    @property
    def still_valid(self):
        return os.path.exists(self.__path)
    
    def open(self, mode=None):
        if mode is None:
            mode = self.__mode
        return DirectoryStorage(self.__path, mode)


class DirectoryStorage(Storage):
    @staticmethod
    def read_storage(path):
        if os.path.isdir(path):
            return DirectoryStorage(os.path.abspath(path), 'r')

    @staticmethod
    def new_storage(path):
        if os.path.isdir(path):
            return DirectoryStorage(os.path.abspath(path), 'w')
    
    def __init__(self, path, mode):
        self.__path = path
        self.__mode = mode
    
    @property
    def path(self):
        return self.__path
    
    def list(self, path=None):
        return os.listdir(self.__fix_path(path))

    def open(self, path, mode='r'):
        if mode != 'r' and self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        path = self.__fix_path(path)
        if mode == 'w':
            self.__create_directory_if_needed(path)
            return open(path, 'wb')
        else:
            if os.path.exists(path):
                return open(path, 'rb')
    
    def store_string(self, path, data):
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        path = self.__fix_path(path)
        self.__create_directory_if_needed(path)
        with open(path, 'w', encoding="ascii") as f:
            f.write(data)
    
    def read_string(self, path):
        path = self.__fix_path(path)
        with open(path, 'r', encoding="ascii") as f:
            return f.read()
    
    def exists(self, path):
        path = self.__fix_path(path)
        return os.path.exists(path)
    
    def create_substorage(self, path):
        path = self.__fix_path(path)
        if os.path.exists(path):
            return Storage.read_storage(path)
    
    def make_dir(self, path):
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        path = self.__fix_path(path)
        os.makedirs(path)
        return DirectoryStorage.new_storage(path)
    
    def get_all_files(self):
        for dirpath, dirs, files in os.walk(self.__path):
            for file in files:
                path = os.path.relpath(os.path.join(dirpath, file), self.__path)
                yield path
    
    def copy_from(self, storage):
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        for path in storage.get_all_files():
            fix_path = self.__fix_path(path)
            self.__create_directory_if_needed(fix_path)
            with storage.open(path) as source_file:
                with open(fix_path, 'wb') as destination_file:
                    destination_file.write(source_file.read())
    
    def __fix_path(self, path):
        if path is None:
            return self.__path
        
        return os.path.join(self.__path, path.lstrip('/'))
    
    def __create_directory_if_needed(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    
    def remember_reference(self):
        return DirectoryStorageReference(self.__path, self.__mode)
    
    def remove_storage(self):
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        shutil.rmtree(self.__path)
    
    def close(self):
        pass
