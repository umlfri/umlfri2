from ..base.type import UflType as UflType

from typing import (
    Any,
    Dict,
    Union,
)
from umlfri2.ufl.types.generic.any import UflAnyType
from umlfri2.ufl.types.generic.anyequatable import UflAnyEquatableType
from umlfri2.ufl.types.generic.anywithdefault import UflAnyWithDefault
from umlfri2.ufl.types.structured.object import UflObjectType

class UflGenericType(UflType):
    def __init__(
        self,
        base_type: Union[UflAnyType, UflAnyEquatableType, UflGenericType, UflAnyWithDefault]
    ) -> None: ...
    def resolve_unknown_generic(
        self,
        generics_cache: Dict[UflGenericType, UflObjectType]
    ) -> UflObjectType: ...
    def resolve_generic(
        self,
        actual_type: UflObjectType,
        generics_cache: Dict[Any, Any]
    ) -> UflObjectType: ...
