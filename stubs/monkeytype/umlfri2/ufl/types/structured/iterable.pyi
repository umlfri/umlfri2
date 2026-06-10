from typing import (
    Any,
    Dict,
    Union,
)
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.generic.any import UflAnyType
from umlfri2.ufl.types.generic.generic import UflGenericType
from umlfri2.ufl.types.structured.list import UflListType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType


class UflIterableType:
    def __init__(
        self,
        item_type: Union[UflStringType, UflGenericType, UflVariableWithMetadataType, UflObjectType, UflAnyType]
    ) -> None: ...
    def is_assignable_from(
        self,
        other: Union[UflListType, UflIterableType]
    ) -> bool: ...
    @property
    def item_type(
        self
    ) -> Union[UflVariableWithMetadataType, UflObjectType]: ...
    def resolve_generic(
        self,
        actual_type: UflListType,
        generics_cache: Dict[Any, Any]
    ) -> UflIterableType: ...
    def resolve_unknown_generic(
        self,
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> UflIterableType: ...
