from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.types.basic.bool import UflBoolType


class UflUnaryNode:
    def __init__(
        self,
        operator: str,
        operand: UflAttributeAccessNode,
        type: Optional[UflBoolType] = ...
    ) -> None: ...
    def _get_params(self) -> Tuple[str, UflAttributeAccessNode]: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[str, UflUnaryNode]: ...
    @property
    def operand(self) -> UflAttributeAccessNode: ...
    @property
    def operator(self) -> str: ...
