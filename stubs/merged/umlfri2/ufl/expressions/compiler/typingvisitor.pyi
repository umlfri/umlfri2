from ..tree import *
from ...compilerhelpers.automultiresolver import resolve_multi_type as resolve_multi_type
from ...macro.standard import STANDARD_MACROS as STANDARD_MACROS
from ...types.basic import UflBoolType as UflBoolType, UflDecimalType as UflDecimalType, UflIntegerType as UflIntegerType, UflNumberType as UflNumberType, UflStringType as UflStringType
from ...types.complex import UflColorType as UflColorType, UflFontType as UflFontType
from ...types.enum import UflTypedEnumType as UflTypedEnumType
from ...types.structured import UflIterableType as UflIterableType, UflNullableType as UflNullableType, UflObjectType as UflObjectType, UflVariableWithMetadataType as UflVariableWithMetadataType
from ..tree.visitor import UflVisitor as UflVisitor
from .macroargumenttypeprovider import MacroArgumentTypeProvider as MacroArgumentTypeProvider
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import ALL_ENUMS as ALL_ENUMS
from umlfri2.types.font import Fonts as Fonts

from typing import (
    Any,
    Dict,
    Union,
)
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.binary import UflBinaryNode
from umlfri2.ufl.expressions.tree.enum import UflEnumNode
from umlfri2.ufl.expressions.tree.expression import UflExpressionNode
from umlfri2.ufl.expressions.tree.literal import UflLiteralNode
from umlfri2.ufl.expressions.tree.macroinvoke import UflMacroInvokeNode
from umlfri2.ufl.expressions.tree.objectmetadataaccess import UflObjectMetadataAccessNode
from umlfri2.ufl.expressions.tree.unary import UflUnaryNode
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.expressions.tree.variabledefinition import UflVariableDefinitionNode
from umlfri2.ufl.expressions.tree.variablemetadataccess import UflVariableMetadataAccessNode
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType

class UflTypingVisitor(UflVisitor):
    def __init__(
        self,
        params: Dict[str, Union[UflObjectType, UflStringType, UflIntegerType, UflVariableWithMetadataType]],
        expected_type: Any
    ) -> None: ...
    def visit_attribute_access(
        self,
        node: UflAttributeAccessNode
    ) -> UflAttributeAccessNode: ...
    def visit_enum(
        self,
        node: UflEnumNode
    ) -> UflEnumNode: ...
    def visit_macro_invoke(
        self,
        node: UflMacroInvokeNode
    ) -> UflMacroInvokeNode: ...
    def visit_technical_variable(self, node) -> None: ...
    def visit_variable(
        self,
        node: UflVariableNode
    ) -> UflVariableNode: ...
    def visit_variable_definition(
        self,
        node: UflVariableDefinitionNode
    ) -> UflVariableDefinitionNode: ...
    def visit_binary(
        self,
        node: UflBinaryNode
    ) -> UflBinaryNode: ...
    def visit_unary(
        self,
        node: UflUnaryNode
    ) -> UflUnaryNode: ...
    def visit_literal(
        self,
        node: UflLiteralNode
    ) -> UflLiteralNode: ...
    def visit_variable_metadata_access(
        self,
        node: UflVariableMetadataAccessNode
    ) -> UflVariableMetadataAccessNode: ...
    def visit_object_metadata_access(
        self,
        node: UflObjectMetadataAccessNode
    ) -> UflObjectMetadataAccessNode: ...
    def visit_unpack(self, node) -> None: ...
    def visit_expression(
        self,
        node: UflExpressionNode
    ) -> UflExpressionNode: ...
    def visit_lambda_expression(self, node) -> None: ...
    def visit_cast(self, node) -> None: ...
    def create_for_lambda(
        self,
        lambda_args: Dict[str, UflObjectType]
    ) -> UflTypingVisitor: ...
