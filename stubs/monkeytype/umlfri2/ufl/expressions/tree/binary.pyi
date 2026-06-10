from typing import (
    Any,
    Optional,
    Union,
)
from umlfri2.ufl.compilerhelpers.lambdainlining.lambdainliningvisitorimpl import LambdaInliningVisitorImpl
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.literal import UflLiteralNode
from umlfri2.ufl.expressions.tree.macroinvoke import UflMacroInvokeNode
from umlfri2.ufl.expressions.tree.unary import UflUnaryNode
from umlfri2.ufl.types.basic.bool import UflBoolType


class UflBinaryNode:
    def __init__(
        self,
        operand1: Union[UflBinaryNode, UflUnaryNode, UflAttributeAccessNode, UflMacroInvokeNode],
        operator: str,
        operand2: Union[UflAttributeAccessNode, UflBinaryNode, UflLiteralNode, UflUnaryNode, UflMacroInvokeNode],
        type: Optional[UflBoolType] = ...
    ) -> None: ...
    def _get_params(self) -> Any: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, LambdaInliningVisitorImpl, UflCompilingVisitor]
    ) -> Union[str, UflBinaryNode]: ...
    @property
    def operand1(
        self
    ) -> Union[UflBinaryNode, UflUnaryNode, UflAttributeAccessNode, UflMacroInvokeNode]: ...
    @property
    def operand2(
        self
    ) -> Union[UflAttributeAccessNode, UflBinaryNode, UflLiteralNode, UflUnaryNode, UflMacroInvokeNode]: ...
    @property
    def operator(self) -> str: ...
