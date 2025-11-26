from __future__ import annotations

from typing import Optional, IO, Iterable, Any


class StorageReference:
    @property
    def name(self) -> str:
        raise NotImplementedError
    
    @property
    def still_valid(self) -> bool:
        raise NotImplementedError
    
    def open(self, mode: Optional[str] = None) -> 'Storage':
        raise NotImplementedError


class UnknownStorageException(Exception):
    pass


class Storage:
    @staticmethod
    def read_storage(path: str) -> 'Storage':
        for subclass in Storage.__subclasses__():
            ret = subclass.read_storage(path)
            if ret is not None:
                return ret
        raise UnknownStorageException("Storage {0} not found".format(path))
    
    def list(self, path: Optional[str] = None) -> Iterable[str]:
        raise NotImplementedError
    
    def open(self, path: str, mode: str = 'r') -> Optional[IO[bytes]]:
        raise NotImplementedError
    
    def store_string(self, path: str, data: str) -> None:
        raise NotImplementedError
    
    def read_string(self, path: str) -> str:
        raise NotImplementedError
    
    def exists(self, path: str) -> bool:
        raise NotImplementedError
    
    def create_substorage(self, path: str) -> Optional['Storage']:
        raise NotImplementedError
    
    def make_dir(self, path: str) -> 'Storage':
        raise NotImplementedError
    
    def get_all_files(self) -> Iterable[str]:
        raise NotImplementedError
    
    def copy_from(self, storage: 'Storage') -> None:
        raise NotImplementedError
    
    def remember_reference(self) -> StorageReference:
        raise NotImplementedError
    
    def remove_storage(self) -> None:
        raise NotImplementedError
    
    def close(self) -> None:
        raise NotImplementedError
    
    def __enter__(self) -> 'Storage':
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
