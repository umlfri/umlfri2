from typing import (
    Optional,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.basic.string import UflStringType


class UflCastNode:
    def __init__(
        self,
        object: Union[UflAttributeAccessNode, UflVariableNode],
        type: Optional[UflStringType] = ...
    ) -> None: ...
    def accept(self, visitor: UflCompilingVisitor) -> str: ...
    @property
    def object(
        self
    ) -> Union[UflAttributeAccessNode, UflVariableNode]: ...
