from typing import (
    Any,
    Union,
)
from umlfri2.ufl.types.enum.definedenum import UflDefinedEnumType
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType

class UflEnumPossibility:
    def __init__(
        self,
        enum: Union[UflTypedEnumType, UflStringEnumType, UflDefinedEnumType],
        name: str,
        value: Any
    ) -> None: ...
    @property
    def enum(self) -> UflStringEnumType: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> Any: ...
