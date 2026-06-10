from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.compilerhelpers.lambdainlining.lambdainliningvisitorimpl import LambdaInliningVisitorImpl
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.enum import UflEnumNode
from umlfri2.ufl.expressions.tree.lambdaexpression import UflLambdaExpressionNode
from umlfri2.ufl.expressions.tree.literal import UflLiteralNode
from umlfri2.ufl.macro.standard.iterator.any import AnyMacro
from umlfri2.ufl.macro.standard.iterator.where import WhereMacro
from umlfri2.ufl.macro.standard.other.changefontstyle import ChangeFontStyleMacro
from umlfri2.ufl.macro.standard.other.stringhastext import StringHasTextMacro
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.structured.iterable import UflIterableType


class UflMacroInvokeNode:
    def __init__(
        self,
        target: Union[UflMacroInvokeNode, UflAttributeAccessNode],
        selector: str,
        arguments: Union[Tuple[UflEnumNode, UflLiteralNode], Tuple[UflLambdaExpressionNode], Tuple[UflEnumNode, UflAttributeAccessNode], Tuple[()]],
        inner_type_invoke: bool,
        macro: Optional[Union[StringHasTextMacro, WhereMacro, ChangeFontStyleMacro, AnyMacro]] = ...,
        type: Optional[Union[UflFontType, UflBoolType, UflIterableType]] = ...
    ) -> None: ...
    def _get_params(
        self
    ) -> Union[Tuple[UflAttributeAccessNode, str, str, UflLambdaExpressionNode], Tuple[UflAttributeAccessNode, str, str, UflEnumNode, UflAttributeAccessNode], Tuple[UflAttributeAccessNode, str, str, UflEnumNode, UflLiteralNode], Tuple[UflAttributeAccessNode, str, str], Tuple[UflMacroInvokeNode, str, str, UflEnumNode, UflAttributeAccessNode]]: ...
    def accept(
        self,
        visitor: Union[LambdaInliningVisitorImpl, UflTypingVisitor, UflCompilingVisitor]
    ) -> Union[str, UflMacroInvokeNode]: ...
    @property
    def arguments(
        self
    ) -> Union[Tuple[UflLambdaExpressionNode], Tuple[UflEnumNode, UflAttributeAccessNode], Tuple[UflEnumNode, UflLiteralNode], Tuple[()]]: ...
    @property
    def inner_type_invoke(self) -> bool: ...
    @property
    def macro(
        self
    ) -> Union[StringHasTextMacro, WhereMacro, ChangeFontStyleMacro, AnyMacro]: ...
    @property
    def selector(self) -> str: ...
    @property
    def target(
        self
    ) -> Union[UflMacroInvokeNode, UflAttributeAccessNode]: ...
