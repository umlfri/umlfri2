from typing import (
    Callable,
    Dict,
    Iterator,
    Union,
)
from umlfri2.ufl.types.base.type import UflType
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType


class CompiledUflExpression:
    def __init__(
        self,
        expression: str,
        expected_type: UflType,
        variables: Dict[str, Union[UflStringType, UflIntegerType, UflObjectType, UflVariableWithMetadataType]]
    ) -> None: ...
    @property
    def compiled_function(self) -> Callable: ...
    @property
    def parameters(self) -> Iterator[str]: ...
    @property
    def type(self) -> UflType: ...
