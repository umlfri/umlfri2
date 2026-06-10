from typing import (
    Callable,
    Optional,
)


class OnlineAddOnHash:
    def __init__(self, fnc: Callable) -> None: ...


class OnlineAddOnLocation:
    def __init__(
        self,
        url: str,
        hash: str,
        hash_type: OnlineAddOnHash,
        arch: None = ...,
        os: None = ...
    ) -> None: ...
    @property
    def is_valid(self) -> bool: ...
