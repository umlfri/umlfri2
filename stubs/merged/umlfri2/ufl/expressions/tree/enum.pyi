from .node import UflNode as UflNode

from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType

class UflEnumNode(UflNode):
    def __init__(
        self,
        enum: str,
        item: str,
        type: Optional[UflTypedEnumType] = ...
    ) -> None: ...
    @property
    def enum(self) -> str: ...
    @property
    def item(self) -> str: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[UflEnumNode, str]: ...
