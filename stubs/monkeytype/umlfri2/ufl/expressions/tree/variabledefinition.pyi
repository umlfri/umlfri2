from typing import (
    Optional,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType


class UflVariableDefinitionNode:
    def __init__(
        self,
        name: str,
        type: Optional[Union[UflVariableWithMetadataType, UflStringType, UflIntegerType, UflObjectType]] = ...
    ) -> None: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[UflVariableDefinitionNode, str]: ...
    @property
    def name(self) -> str: ...
