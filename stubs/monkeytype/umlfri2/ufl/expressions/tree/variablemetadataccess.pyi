from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.structured.variablemetadata import UflVariableMetadataType


class UflVariableMetadataAccessNode:
    def __init__(
        self,
        obj: UflVariableNode,
        type: Optional[UflVariableMetadataType] = ...
    ) -> None: ...
    def _get_params(self) -> Tuple[UflVariableNode]: ...
    def accept(
        self,
        visitor: Union[UflCompilingVisitor, UflTypingVisitor]
    ) -> Union[UflVariableMetadataAccessNode, str]: ...
    @property
    def object(self) -> UflVariableNode: ...
