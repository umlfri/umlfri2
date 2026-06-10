from typing import Union
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType


class UflAnyType:
    def is_assignable_from(
        self,
        other: Union[UflObjectType, UflStringEnumType, UflVariableWithMetadataType]
    ) -> bool: ...
