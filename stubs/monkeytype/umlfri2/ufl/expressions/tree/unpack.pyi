from typing import Optional
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.structured.object import UflObjectType


class UflUnpackNode:
    def __init__(
        self,
        object: UflVariableNode,
        type: Optional[UflObjectType] = ...
    ) -> None: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
    @property
    def object(self) -> UflVariableNode: ...
