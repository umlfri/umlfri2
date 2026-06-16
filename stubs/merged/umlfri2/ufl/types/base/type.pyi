from _typeshed import Incomplete
from typing import NamedTuple

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

class UflAttributeDescription(NamedTuple):
    accessor: Incomplete
    type: Incomplete

class UflType:
    ALLOWED_DIRECT_ATTRIBUTES: Incomplete
    @property
    def parent(self) -> Any: ...
    @property
    def has_default(self): ...
    def build_default(self, generator) -> None: ...
    def is_assignable_from(self, other: UflType) -> bool: ...
    def set_parent(self, parent: Any) -> None: ...
    @property
    def is_immutable(self) -> None: ...
    def is_convertible_to(self, other): ...
    def is_equatable_to(self, other): ...
    def is_comparable_with(self, other): ...
    def is_valid_value(self, value) -> None: ...
    def is_default_value(self, value) -> None: ...
    def resolve_unknown_generic(
        self,
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> Union[UflBoolType, UflFontType]: ...
    def resolve_generic(
        self,
        actual_type: Union[UflBoolType, UflStringType, UflTypedEnumType, UflFontType],
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> Union[UflBoolType, UflStringType, UflTypedEnumType, UflFontType]: ...
