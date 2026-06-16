from ...macro.argumenttypechecker import ArgumentTypeChecker as ArgumentTypeChecker, ArgumentTypeCheckerResult as ArgumentTypeCheckerResult
from ...types.executable import UflLambdaType as UflLambdaType
from ...types.structured import UflVariableWithMetadataType as UflVariableWithMetadataType
from ..tree import UflLambdaExpressionNode as UflLambdaExpressionNode, UflUnpackNode as UflUnpackNode
from _typeshed import Incomplete
from collections.abc import Generator

from typing import (
    Iterator,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.enum import UflEnumNode
from umlfri2.ufl.expressions.tree.lambdaexpression import UflLambdaExpressionNode
from umlfri2.ufl.expressions.tree.literal import UflLiteralNode
from umlfri2.ufl.macro.argumenttypechecker import ArgumentTypeCheckerResult
from umlfri2.ufl.macro.signature import FoundSignature
from umlfri2.ufl.types.basic.bool import UflBoolType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType
from umlfri2.ufl.types.executable.ufllambda import UflLambdaType
from umlfri2.ufl.types.structured.iterable import UflIterableType
from umlfri2.ufl.types.structured.list import UflListType

class MacroArgumentTypeProvider(ArgumentTypeChecker):
    def __init__(
        self,
        target_type: Union[UflStringType, UflFontType, UflListType],
        expressions: Union[Tuple[UflLambdaExpressionNode], Tuple[()], Tuple[UflEnumNode, UflLiteralNode], Tuple[UflEnumNode, UflAttributeAccessNode]],
        typing_visitor: UflTypingVisitor
    ) -> None: ...
    def check_arguments(
        self,
        self_type: Union[UflIterableType, UflFontType, UflStringType],
        expected_types: Union[Tuple[UflLambdaType], Tuple[UflTypedEnumType, UflBoolType], Tuple[()]],
        return_type: Union[UflIterableType, UflBoolType, UflFontType]
    ) -> ArgumentTypeCheckerResult: ...
    def resolve_for(
        self,
        found_signature: FoundSignature
    ) -> Iterator[Union[UflEnumNode, UflLiteralNode, UflAttributeAccessNode, UflLambdaExpressionNode]]: ...
