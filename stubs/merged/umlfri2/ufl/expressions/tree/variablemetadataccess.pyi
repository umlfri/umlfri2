from .node import UflNode as UflNode

from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.structured.variablemetadata import UflVariableMetadataType

class UflVariableMetadataAccessNode(UflNode):
    def __init__(
        self,
        obj: UflVariableNode,
        type: Optional[UflVariableMetadataType] = ...
    ) -> None: ...
    @property
    def object(self) -> UflVariableNode: ...
    def accept(
        self,
        visitor: Union[UflCompilingVisitor, UflTypingVisitor]
    ) -> Union[UflVariableMetadataAccessNode, str]: ...
