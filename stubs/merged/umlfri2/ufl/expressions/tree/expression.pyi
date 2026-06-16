from .node import UflNode as UflNode
from _typeshed import Incomplete
from collections.abc import Generator

from typing import (
    Any,
    Iterator,
    Optional,
    Tuple,
    Union,
)
from umlfri2.ufl.expressions.compiler.compilingvisitor import UflCompilingVisitor
from umlfri2.ufl.expressions.compiler.typingvisitor import UflTypingVisitor
from umlfri2.ufl.expressions.tree.node import UflNode
from umlfri2.ufl.expressions.tree.variabledefinition import UflVariableDefinitionNode

class UflExpressionNode(UflNode):
    def __init__(
        self,
        result: UflNode,
        variables: Union[Tuple[UflVariableDefinitionNode, UflVariableDefinitionNode], Tuple[UflVariableDefinitionNode]],
        type: Optional[Any] = ...
    ) -> None: ...
    @property
    def result(self) -> UflNode: ...
    @property
    def variables(self) -> Iterator[UflVariableDefinitionNode]: ...
    def accept(
        self,
        visitor: Union[UflCompilingVisitor, UflTypingVisitor]
    ) -> Union[str, UflExpressionNode]: ...
