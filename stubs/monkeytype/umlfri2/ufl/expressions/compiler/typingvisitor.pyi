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


class UflTypingVisitor:
    def __init__(
        self,
        params: Dict[str, Union[UflObjectType, UflStringType, UflIntegerType, UflVariableWithMetadataType]],
        expected_type: Any
    ) -> None: ...
    def create_for_lambda(
        self,
        lambda_args: Dict[str, UflObjectType]
    ) -> UflTypingVisitor: ...
    def visit_attribute_access(
        self,
        node: UflAttributeAccessNode
    ) -> UflAttributeAccessNode: ...
    def visit_binary(
        self,
        node: UflBinaryNode
    ) -> UflBinaryNode: ...
    def visit_enum(
        self,
        node: UflEnumNode
    ) -> UflEnumNode: ...
    def visit_expression(
        self,
        node: UflExpressionNode
    ) -> UflExpressionNode: ...
    def visit_literal(
        self,
        node: UflLiteralNode
    ) -> UflLiteralNode: ...
    def visit_macro_invoke(
        self,
        node: UflMacroInvokeNode
    ) -> UflMacroInvokeNode: ...
    def visit_object_metadata_access(
        self,
        node: UflObjectMetadataAccessNode
    ) -> UflObjectMetadataAccessNode: ...
    def visit_unary(
        self,
        node: UflUnaryNode
    ) -> UflUnaryNode: ...
    def visit_variable(
        self,
        node: UflVariableNode
    ) -> UflVariableNode: ...
    def visit_variable_definition(
        self,
        node: UflVariableDefinitionNode
    ) -> UflVariableDefinitionNode: ...
    def visit_variable_metadata_access(
        self,
        node: UflVariableMetadataAccessNode
    ) -> UflVariableMetadataAccessNode: ...
