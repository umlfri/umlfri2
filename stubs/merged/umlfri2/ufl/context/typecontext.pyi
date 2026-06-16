from umlfri2.ufl.types.enum import UflDefinedEnumType as UflDefinedEnumType
from umlfri2.ufl.types.structured import UflNullableType as UflNullableType

from typing import (
    Dict,
    Optional,
    Union,
)
from umlfri2.ufl.components.connectionvisual.arrow import ArrowDefinition
from umlfri2.ufl.components.visual.rectangle import (
    CornerDefinition,
    SideDefinition,
)
from umlfri2.ufl.types.base.type import UflType
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType

class TypeContext:
    def __init__(
        self,
        definitions: Dict[str, Union[Dict[str, ArrowDefinition], Dict[str, CornerDefinition], Dict[str, SideDefinition]]]
    ) -> None: ...
    def get_variable_type(self, name): ...
    def as_dict(
        self,
        prefix: None = ...
    ) -> Dict[str, Union[UflStringType, UflIntegerType, UflObjectType, UflVariableWithMetadataType]]: ...
    def set_variable_type(
        self,
        name: str,
        type: Union[UflVariableWithMetadataType, UflStringType, UflIntegerType, UflObjectType]
    ) -> TypeContext: ...
