from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.types.basic.string import UflStringType


class UflStringEnumType:
    def __init__(
        self,
        possibilities: Union[Tuple[str, str, str, str, str], Tuple[str, str, str, str]],
        default: Optional[str] = ...
    ) -> None: ...
    def is_convertible_to(self, other: UflStringType) -> bool: ...
    def is_equatable_to(self, other: UflStringType) -> bool: ...
