from .node import UflNode as UflNode

from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.compilerhelpers.lambdainlining.lambdainliningvisitorimpl import LambdaInliningVisitorImpl
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.technicalvariable import UflTechnicalVariableNode
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableWithMetadataType

class UflVariableNode(UflNode):
    def __init__(
        self,
        name: str,
        type: Optional[Union[UflIntegerType, UflObjectType, UflStringType, UflVariableWithMetadataType]] = ...
    ) -> None: ...
    @property
    def name(self) -> str: ...
    def accept(
        self,
        visitor: Union[UflTypingVisitor, UflCompilingVisitor, LambdaInliningVisitorImpl]
    ) -> Union[UflVariableNode, UflTechnicalVariableNode, str]: ...
