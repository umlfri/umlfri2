from _typeshed import Incomplete
from collections.abc import Generator

from typing import (
    Any,
    Callable,
    Iterator,
)
from umlfri2.ufl.expressions.tree.variable import UflVariableNode
from umlfri2.ufl.types.base.type import UflType

class UflNode:
    def __init__(self, type: Any) -> None: ...
    @property
    def type(self) -> UflType: ...
    def find(
        self,
        condition: Callable,
        cut_branch: Callable = ...
    ) -> Iterator[UflVariableNode]: ...
    def to_string_indented(self, indent: int = 0): ...
    def accept(self, visitor) -> None: ...
