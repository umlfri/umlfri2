from typing import (
    Callable,
    Dict,
    Type,
    Union,
)
from umlfri2.types.enums.fontstyle import FontStyle
from umlfri2.ufl.expressions.tree.attributeaccess import UflAttributeAccessNode
from umlfri2.ufl.expressions.tree.binary import UflBinaryNode
from umlfri2.ufl.expressions.tree.cast import UflCastNode
from umlfri2.ufl.expressions.tree.enum import UflEnumNode
from umlfri2.ufl.expressions.tree.expression import UflExpressionNode
from umlfri2.ufl.expressions.tree.literal import UflLiteralNode
from umlfri2.ufl.expressions.tree.macroinvoke import UflMacroInvokeNode
from umlfri2.ufl.expressions.tree.objectmetadataaccess import UflObjectMetadataAccessNode
from umlfri2.ufl.expressions.tree.technicalvariable import UflTechnicalVariableNode
from umlfri2.ufl.expressions.tree.unary import UflUnaryNode
from umlfri2.ufl.expressions.tree.unpack import UflUnpackNode
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.expressions.tree.variabledefinition import UflVariableDefinitionNode
from umlfri2.ufl.expressions.tree.variablemetadataccess import UflVariableMetadataAccessNode


class UflCompilingVisitor:
    def __init__(self, variable_prefix: str) -> None: ...
    @property
    def all_globals(
        self
    ) -> Dict[str, Union[Callable, Type[bool], Type[str], Type[FontStyle]]]: ...
    def visit_attribute_access(self, node: UflAttributeAccessNode) -> str: ...
    def visit_binary(self, node: UflBinaryNode) -> str: ...
    def visit_cast(self, node: UflCastNode) -> str: ...
    def visit_enum(self, node: UflEnumNode) -> str: ...
    def visit_expression(self, node: UflExpressionNode) -> str: ...
    def visit_literal(self, node: UflLiteralNode) -> str: ...
    def visit_macro_invoke(self, node: UflMacroInvokeNode) -> str: ...
    def visit_object_metadata_access(
        self,
        node: UflObjectMetadataAccessNode
    ) -> str: ...
    def visit_technical_variable(
        self,
        node: UflTechnicalVariableNode
    ) -> str: ...
    def visit_unary(self, node: UflUnaryNode) -> str: ...
    def visit_unpack(self, node: UflUnpackNode) -> str: ...
    def visit_variable(self, node: UflVariableNode) -> str: ...
    def visit_variable_definition(
        self,
        node: UflVariableDefinitionNode
    ) -> str: ...
    def visit_variable_metadata_access(
        self,
        node: UflVariableMetadataAccessNode
    ) -> str: ...
