from typing import (
    Any,
    Union,
)
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.complex.color import UflColorType
from umlfri2.ufl.types.enum.definedenum import UflDefinedEnumType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType


class UflNullableType:
    def __init__(self, inner_type: Any) -> None: ...
    @property
    def inner_type(
        self
    ) -> Union[UflTypedEnumType, UflColorType, UflIntegerType, UflDefinedEnumType]: ...
    def is_assignable_from(
        self,
        other: Union[UflColorType, UflNullableType]
    ) -> bool: ...
    def parse(self, value: str) -> Any: ...
