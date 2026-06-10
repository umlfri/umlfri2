from typing import (
    Iterator,
    List,
    Optional,
    Union,
)
from umlfri2.ufl.compilerhelpers.lambdainlining.lambdainliningvisitor import LambdaInliningVisitor
from umlfri2.ufl.expressions.tree.binary import UflBinaryNode
from umlfri2.ufl.expressions.tree.macroinvoke import UflMacroInvokeNode
from umlfri2.ufl.types.executable.ufllambda import UflLambdaType


class UflLambdaExpressionNode:
    def __init__(
        self,
        body: Union[UflBinaryNode, UflMacroInvokeNode],
        parameters: List[str],
        type: Optional[UflLambdaType] = ...
    ) -> None: ...
    def accept(
        self,
        visitor: LambdaInliningVisitor
    ) -> Union[UflBinaryNode, UflMacroInvokeNode]: ...
    @property
    def body(
        self
    ) -> Union[UflBinaryNode, UflMacroInvokeNode]: ...
    @property
    def parameter_count(self) -> int: ...
    @property
    def parameters(self) -> Iterator[str]: ...
