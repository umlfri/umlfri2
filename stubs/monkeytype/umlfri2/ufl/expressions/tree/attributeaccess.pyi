from typing import (
    Any,
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.compilerhelpers.lambdainlining.lambdainliningvisitorimpl import LambdaInliningVisitorImpl
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.technicalvariable import UflTechnicalVariableNode
from umlfri2.ufl.expressions.tree.unpack import UflUnpackNode
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.expressions.tree.variablemetadataccess import UflVariableMetadataAccessNode


class UflAttributeAccessNode:
    def __init__(
        self,
        obj: Union[UflVariableMetadataAccessNode, UflVariableNode, UflUnpackNode, UflAttributeAccessNode, UflTechnicalVariableNode],
        attribute: str,
        type: Optional[Any] = ...
    ) -> None: ...
    def _get_params(
        self
    ) -> Union[Tuple[UflVariableMetadataAccessNode, str], Tuple[UflVariableNode, str], Tuple[UflAttributeAccessNode, str]]: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, LambdaInliningVisitorImpl, UflCompilingVisitor]
    ) -> Union[UflAttributeAccessNode, str]: ...
    @property
    def attribute(self) -> str: ...
    @property
    def object(
        self
    ) -> Union[UflVariableMetadataAccessNode, UflVariableNode, UflUnpackNode, UflAttributeAccessNode, UflTechnicalVariableNode]: ...
