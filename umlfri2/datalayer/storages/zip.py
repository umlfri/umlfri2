import os.path
import zipfile
import itertools
from .storage import Storage


class ZipStorage(Storage):
    @staticmethod
    def open(path):
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
                z = open(os.path.join(*zip_path), 'rb')
                return ZipStorage(zipfile.ZipFile(z), file_path)
        
    def __init__(self, zip_file, path):
        self.__zip_file = zip_file
        self.__path = path
    
    def list(self, path=None):
        path = self.__fix_path(path)
        for name in self.__zip_file.namelist():
            if os.path.dirname(name) == path:
                yield os.path.basename(name)
    
    def read(self, path):
        return self.__zip_file.open(self.__fix_path(path))
    
    def exists(self, path):
        return self.__fix_path(path) in self.__zip_file.namelist()
    
    def sub_open(self, path):
        if self.__dir_exists(path):
            return ZipStorage(self.__zip_file, self.__fix_path_list(path))
    
    def get_all_files(self):
        path = self.__fix_path('')
        for name in self.__zip_file.namelist():
            if name.startswith(path) and not name.endswith('/'):
                yield name[len(path):]
    
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
