import os.path
import zipfile
import itertools
from io import BytesIO
from typing import Optional, Iterable, IO, List, Any

from .storage import Storage, StorageReference


class ZipStorageReference(StorageReference):
    def __init__(self, zip_path: str, path: List[str], mode: str) -> None:
        self.__zip_path = zip_path
        self.__path = path
        self.__mode = mode
    
    @property
    def name(self) -> str:
        return self.__zip_path
    
    @property
    def still_valid(self) -> bool:
        return os.path.exists(os.path.dirname(self.__zip_path))
    
    def open(self, mode: Optional[str] = None) -> 'ZipStorage':
        if mode is None:
            mode = self.__mode
        z = open(self.__zip_path, mode + 'b')
        return ZipStorage(self.__zip_path, zipfile.ZipFile(z, mode=mode, compression=zipfile.ZIP_DEFLATED),
                          self.__path, mode)


class ZipFileWriter(BytesIO):
    def __init__(self, zip_file: zipfile.ZipFile, file_path: str) -> None:
        super().__init__()
        self.__zip_file = zip_file
        self.__file_path = file_path
        self.__closed = False
    
    def __enter__(self) -> 'ZipFileWriter':
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self.__closed:
            self.close()
    
    def close(self) -> None:
        super().flush()
        self.__zip_file.writestr(self.__file_path, self.getvalue())
        super().close()
        self.__closed = True


class ZipStorage(Storage):
    @staticmethod
    def read_storage(path: str) -> Optional['ZipStorage']:
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
            
            zip_path_joined = os.path.join(*zip_path)
            
            if zip_path[0] == "":
                zip_path_joined = os.path.sep + zip_path_joined
            
            if zipfile.is_zipfile(zip_path_joined):
                z = open(zip_path_joined, 'rb')
                return ZipStorage(zip_path_joined, zipfile.ZipFile(z, mode='r', compression=zipfile.ZIP_DEFLATED),
                                  file_path, 'r')
    
    @staticmethod
    def new_storage(path: str) -> 'ZipStorage':
        z = open(path, 'wb')
        zip_file = zipfile.ZipFile(z, mode='w', compression=zipfile.ZIP_DEFLATED)
        return ZipStorage(path, zip_file, [], 'w')
    
    @staticmethod
    def read_from_memory(bytes: bytes) -> 'ZipStorage':
        z = BytesIO(bytes)
        zip_file = zipfile.ZipFile(z, mode='r')
        return ZipStorage(None, zip_file, [], 'r')
    
    def __init__(self, zip_path: Optional[str], zip_file: zipfile.ZipFile, path: List[str], mode: str) -> None:
        self.__zip_path = zip_path
        self.__zip_file = zip_file
        self.__path = path
        self.__mode = mode
    
    def list(self, path: str = '/') -> Iterable[str]:
        path = self.__fix_path(path)
        for name in self.__zip_file.namelist():
            name = name.rstrip('/')
            if os.path.dirname(name) == path:
                yield os.path.basename(name)
    
    def open(self, path: str, mode: str = 'r') -> IO[bytes]:
        if mode == 'r':
            return self.__zip_file.open(self.__fix_path(path))
        elif mode == 'w':
            if self.__mode == 'r':
                raise ValueError("Storage is opened for read only")
            return ZipFileWriter(self.__zip_file, path)
    
    def store_string(self, path: str, data: str) -> None:
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        
        self.__zip_file.writestr(self.__fix_path(path), data.encode("ascii"), compress_type=zipfile.ZIP_STORED)
    
    def read_string(self, path: str) -> str:
        return self.__zip_file.read(self.__fix_path(path)).decode("ascii")
    
    def exists(self, path: str) -> bool:
        return self.__fix_path(path) in self.__zip_file.namelist()
    
    def create_substorage(self, path: str) -> Optional['ZipStorage']:
        if self.__dir_exists(path):
            return ZipStorage(self.__zip_path, self.__zip_file, self.__fix_path_list(path), self.__mode)

    def make_dir(self, path: str) -> 'ZipStorage':
        return ZipStorage(self.__zip_path, self.__zip_file, self.__fix_path_list(path), self.__mode)
    
    def get_all_files(self) -> Iterable[str]:
        path = self.__fix_path('')
        for name in self.__zip_file.namelist():
            if name.startswith(path) and not name.endswith('/'):
                yield name[len(path):]
    
    def copy_from(self, storage: Storage) -> None:
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        for path in storage.get_all_files():
            with storage.open(path) as source_file:
                self.__zip_file.writestr(self.__fix_path(path), source_file.read())
    
    def remember_reference(self) -> ZipStorageReference:
        if self.__zip_path is None:
            raise Exception("Cannot remember reference to in-memory zip storage")
        return ZipStorageReference(self.__zip_path, self.__path, self.__mode)
    
    def remove_storage(self) -> None:
        if self.__mode == 'r':
            raise ValueError("Storage is opened for read only")
        if self.__path:
            raise ValueError("Cannot remove zip sub-storage")
        
        os.unlink(self.__zip_path)
    
    def close(self) -> None:
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
