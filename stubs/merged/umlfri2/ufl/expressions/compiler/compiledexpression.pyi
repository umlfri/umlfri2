from ..parser import parse_ufl as parse_ufl
from .compilingvisitor import UflCompilingVisitor as UflCompilingVisitor
from .typingvisitor import UflTypingVisitor as UflTypingVisitor
from _typeshed import Incomplete
from collections.abc import Generator

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
    def source(self): ...
    @property
    def parameters(self) -> Iterator[str]: ...
    @property
    def compiled_source(self): ...
    @property
    def compiled_function(self) -> Callable: ...
    @property
    def type(self) -> UflType: ...
