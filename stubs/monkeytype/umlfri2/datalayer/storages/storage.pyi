from typing import Union
from umlfri2.datalayer.storages.directory import DirectoryStorage
from umlfri2.datalayer.storages.zip import ZipStorage


class Storage:
    def __enter__(
        self
    ) -> Union[ZipStorage, DirectoryStorage]: ...
    def __exit__(self, exc_type: None, exc_val: None, exc_tb: None) -> None: ...
    @staticmethod
    def read_storage(
        path: str
    ) -> Union[ZipStorage, DirectoryStorage]: ...
