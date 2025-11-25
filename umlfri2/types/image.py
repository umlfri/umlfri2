from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from umlfri2.datalayer.storages import Storage


class Image:
    def __init__(self, storage: Storage, path: str) -> None:
        self.__storage = storage
        self.__path = path
    
    @property
    def storage(self) -> Storage:
        return self.__storage
    
    @property
    def path(self) -> str:
        return self.__path
    
    def load(self) -> BinaryIO:
        return self.__storage.open(self.__path)
    
    def __repr__(self) -> str:
        return "<Icon {0}>".format(self.__path)
