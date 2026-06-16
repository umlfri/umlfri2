from .node import UflNode as UflNode

from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.string import UflStringType

class UflLiteralNode(UflNode):
    def __init__(
        self,
        value: Union[str, bool],
        type: Optional[Union[UflStringType, UflBoolType]] = ...
    ) -> None: ...
    @property
    def value(self) -> Union[str, bool]: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[UflLiteralNode, str]: ...
