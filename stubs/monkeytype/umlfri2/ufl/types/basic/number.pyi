from typing import (
    Optional,
    Union,
)
from umlfri2.ufl.types.basic.string import UflStringType


class UflNumberType:
    def __init__(self, default: None = ...) -> None: ...
    def is_convertible_to(self, other: UflStringType) -> bool: ...
    def parse(self, value: Union[str, int]) -> Union[float, int]: ...
