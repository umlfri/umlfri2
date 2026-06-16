from ..base.type import UflAttributeDescription as UflAttributeDescription, UflType as UflType
from _typeshed import Incomplete
from collections.abc import Generator

from typing import (
    Dict,
    Iterator,
    Tuple,
    Union,
)
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.image import UflImageType
from umlfri2.ufl.types.generic.any import UflAnyType
from umlfri2.ufl.types.structured.iterable import UflIterableType
from umlfri2.ufl.types.structured.object import UflObjectType

class UflVariableMetadataType(UflType):
    ALLOWED_DIRECT_ATTRIBUTES: Incomplete
    def __init__(
        self,
        metadata_type: Dict[str, Union[UflImageType, UflStringType, UflIterableType, UflIntegerType, UflBoolType]],
        underlying_type: Union[UflObjectType, UflVariableWithMetadataType]
    ) -> None: ...
    @property
    def is_immutable(self): ...

class UflVariableWithMetadataType(UflType):
    VALUE_ATTRIBUTE: str
    def __init__(
        self,
        underlying_type: Union[UflObjectType, UflAnyType, UflVariableWithMetadataType],
        **metadata_types
    ) -> None: ...
    @property
    def metadata_types(
        self
    ) -> Iterator[Union[Tuple[str, UflImageType], Tuple[str, UflStringType], Tuple[str, UflIterableType]]]: ...
    @property
    def underlying_type(
        self
    ) -> Union[UflAnyType, UflObjectType]: ...
    @property
    def metadata_type(self) -> UflVariableMetadataType: ...
    def is_equatable_to(self, other): ...
    def is_comparable_with(self, other): ...
    def is_convertible_to(self, other): ...
    def resolve_unknown_generic(self, generics_cache) -> None: ...
    def resolve_generic(self, actual_type, generics_cache) -> None: ...
