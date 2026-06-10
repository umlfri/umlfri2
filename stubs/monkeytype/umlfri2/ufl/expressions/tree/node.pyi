from typing import (
    Any,
    Callable,
    Iterator,
)
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.base.type import UflType


class UflNode:
    def __init__(self, type: Any) -> None: ...
    def find(
        self,
        condition: Callable,
        cut_branch: Callable = ...
    ) -> Iterator[UflVariableNode]: ...
    @property
    def type(self) -> UflType: ...
