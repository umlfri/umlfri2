from typing import (
    Any,
    Dict,
    Union,
)
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType
from umlfri2.ufl.types.generic.generic import UflGenericType
from umlfri2.ufl.types.structured.object import UflObjectType


class UflType:
    def is_assignable_from(self, other: UflType) -> bool: ...
    @property
    def parent(self) -> Any: ...
    def resolve_generic(
        self,
        actual_type: Union[UflBoolType, UflStringType, UflTypedEnumType, UflFontType],
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> Union[UflBoolType, UflStringType, UflTypedEnumType, UflFontType]: ...
    def resolve_unknown_generic(
        self,
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> Union[UflBoolType, UflFontType]: ...
    def set_parent(self, parent: Any) -> None: ...
