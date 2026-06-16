from .node import UflNode as UflNode

from typing import Optional
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.structured.object import UflObjectType

class UflUnpackNode(UflNode):
    def __init__(
        self,
        object: UflVariableNode,
        type: Optional[UflObjectType] = ...
    ) -> None: ...
    @property
    def object(self) -> UflVariableNode: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
