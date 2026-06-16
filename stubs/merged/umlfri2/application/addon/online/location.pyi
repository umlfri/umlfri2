from enum import Enum
from typing import (
    Callable,
    Optional,
)


class OnlineAddOnArch(Enum):
    processor_32 = 1
    processor_64 = 2

class OnlineAddOnHash(Enum):
    sha256 = ...
    def __init__(self, fnc: Callable) -> None: ...
    def compute(self, bytes): ...

class OnlineAddOnLocation:
    def __init__(
        self,
        url: str,
        hash: str,
        hash_type: OnlineAddOnHash,
        arch: None = None,
        os: None = None
    ) -> None: ...
    @property
    def url(self): ...
    @property
    def is_valid(self) -> bool: ...
    def download(self): ...
