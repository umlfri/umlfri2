from .node import UflNode as UflNode

from typing import (
    Optional,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.basic.string import UflStringType

class UflCastNode(UflNode):
    def __init__(
        self,
        object: Union[UflAttributeAccessNode, UflVariableNode],
        type: Optional[UflStringType] = ...
    ) -> None: ...
    @property
    def object(
        self
    ) -> Union[UflAttributeAccessNode, UflVariableNode]: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
