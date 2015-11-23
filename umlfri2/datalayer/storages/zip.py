import os.path
import zipfile
import itertools
from io import BytesIO

from .storage import Storage, StorageReference


class ZipStorageReference(StorageReference):
    def __init__(self, zip_path, path, mode):
        self.__zip_path = zip_path
        self.__path = path
        self.__mode = mode
    
    def open(self):
        z = open(self.__zip_path, self.__mode + 'b')
        return ZipStorage(self.__zip_path, zipfile.ZipFile(z, mode=self.__mode), self.__path, self.__mode)


class ZipFileWriter(BytesIO):
    def __init__(self, zip_file, file_path): 
        super().__init__()
        self.__zip_file = zip_file
        self.__file_path = file_path
        self.__closed = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__closed:
            self.close()
    
    def close(self):
        super().flush()
        self.__zip_file.writestr(self.__file_path, self.getvalue())
        super().close()
        self.__closed = True


class ZipStorage(Storage):
    @staticmethod
    def create_storage(path, mode='r'):
        if os.path.isdir(path):
            return None
        
        drive, path = os.path.splitdrive(path)
        
        if drive:
            zip_path = [drive + os.path.sep]
        else:
            zip_path = []
        
        if os.path.altsep:
            path = path.replace(os.path.altsep, os.path.sep)
        
        file_path = path.split(os.path.sep)
        
        while True:
            if not file_path:
                return None
            
            zip_path.append(file_path.pop(0))
            
            if zipfile.is_zipfile(os.path.join(*zip_path)):
                z_path = os.path.join(*zip_path)
                z = open(z_path, mode+'b')
                return ZipStorage(z_path, zipfile.ZipFile(z, mode=mode), file_path, mode)
    
    @staticmethod
    def new_storage(path):
        z = open(path, 'wb')
        return ZipStorage(path, zipfile.ZipFile(z, mode='w'), [], 'w')
    
    def __init__(self, zip_path, zip_file, path, mode):
        self.__zip_path = zip_path
        self.__zip_file = zip_file
        self.__path = path
        self.__mode = mode
    
    def list(self, path=None):
        path = self.__fix_path(path)
        for name in self.__zip_file.namelist():
            if os.path.dirname(name) == path:
                yield os.path.basename(name)
    
    def open(self, path, mode='r'):
        if mode == 'r':
            return self.__zip_file.open(self.__fix_path(path))
        elif mode == 'w':
            if self.__mode == 'r':
                raise ValueError("Storage is opened for read only")
            return ZipFileWriter(self.__zip_file, path)
    
    def exists(self, path):
        return self.__fix_path(path) in self.__zip_file.namelist()
    
    def create_substorage(self, path):
        if self.__dir_exists(path):
            return ZipStorage(self.__zip_path, self.__zip_file, self.__fix_path_list(path))
    
    def get_all_files(self):
        path = self.__fix_path('')
        for name in self.__zip_file.namelist():
            if name.startswith(path) and not name.endswith('/'):
                yield name[len(path):]
    
    def remember_reference(self):
        return ZipStorageReference(self.__zip_path, self.__path, self.__mode)
    
    def close(self):
        self.__zip_file.close()
    
    def __dir_exists(self, path):
        return (self.__fix_path(path) + '/') in self.__zip_file.namelist()

    def __fix_path(self, path):
        return '/'.join(self.__fix_path_list(path))

    def __fix_path_list(self, path):
        if path is None:
            return self.__path
        
        ret = []
        for part in itertools.chain(self.__path, path.split('/')):
            if part == '..':
                del ret[-1]
            elif part and part != '.':
                ret.append(part)
        return ret
