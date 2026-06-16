from ...compilerhelpers.automultiresolver import resolve_multi_source as resolve_multi_source, resolve_multi_type as resolve_multi_type
from ...macro.inlined import InlinedMacro as InlinedMacro
from ...types.basic import UflStringType as UflStringType
from ...types.complex import UflColorType as UflColorType, UflFontType as UflFontType
from ...types.enum import UflTypedEnumType as UflTypedEnumType
from ...types.structured import UflVariableWithMetadataType as UflVariableWithMetadataType
from ..tree.visitor import UflVisitor as UflVisitor
from .varnameregister import VariableNameRegister as VariableNameRegister
from umlfri2.types.color import Colors as Colors
from umlfri2.types.enums import ALL_ENUMS as ALL_ENUMS
from umlfri2.types.font import Fonts as Fonts

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

class UflCompilingVisitor(UflVisitor):
    def __init__(self, variable_prefix: str) -> None: ...
    def visit_attribute_access(self, node: UflAttributeAccessNode) -> str: ...
    def visit_enum(self, node: UflEnumNode) -> str: ...
    def visit_macro_invoke(self, node: UflMacroInvokeNode) -> str: ...
    def visit_technical_variable(
        self,
        node: UflTechnicalVariableNode
    ) -> str: ...
    def visit_variable(self, node: UflVariableNode) -> str: ...
    def visit_variable_definition(
        self,
        node: UflVariableDefinitionNode
    ) -> str: ...
    def visit_binary(self, node: UflBinaryNode) -> str: ...
    def visit_unary(self, node: UflUnaryNode) -> str: ...
    def visit_literal(self, node: UflLiteralNode) -> str: ...
    def visit_variable_metadata_access(
        self,
        node: UflVariableMetadataAccessNode
    ) -> str: ...
    def visit_object_metadata_access(
        self,
        node: UflObjectMetadataAccessNode
    ) -> str: ...
    def visit_unpack(self, node: UflUnpackNode) -> str: ...
    def visit_expression(self, node: UflExpressionNode) -> str: ...
    def visit_lambda_expression(self, node): ...
    def visit_cast(self, node: UflCastNode) -> str: ...
    @property
    def all_globals(
        self
    ) -> Dict[str, Union[Callable, Type[bool], Type[str], Type[FontStyle]]]: ...
