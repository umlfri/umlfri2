from ..base.type import UflType as UflType

from typing import Union
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType

class UflAnyType(UflType):
    def is_assignable_from(
        self,
        other: Union[UflObjectType, UflStringEnumType, UflVariableWithMetadataType]
    ) -> bool: ...
    def resolve_unknown_generic(self, generics_cache) -> None: ...
    def resolve_generic(self, actual_type, generics_cache): ...
