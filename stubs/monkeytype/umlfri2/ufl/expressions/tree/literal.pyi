from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.string import UflStringType


class UflLiteralNode:
    def __init__(
        self,
        value: Union[str, bool],
        type: Optional[Union[UflStringType, UflBoolType]] = ...
    ) -> None: ...
    def _get_params(self) -> Union[Tuple[str], Tuple[bool]]: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[UflLiteralNode, str]: ...
    @property
    def value(self) -> Union[str, bool]: ...
