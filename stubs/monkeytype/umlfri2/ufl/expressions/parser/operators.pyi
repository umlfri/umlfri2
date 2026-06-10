from pyparsing.results import ParseResults
from typing import (
    Optional,
    Type,
)
from umlfri2.ufl.expressions.tree.binary import UflBinaryNode
from umlfri2.ufl.expressions.tree.node import UflNode
from umlfri2.ufl.expressions.tree.unary import UflUnaryNode


def get_binary_operator(operator: Optional[str]) -> Optional[str]: ...


def get_priority(operator: str) -> int: ...


def get_unary_operator(operator: str) -> str: ...


def make_binary_operator_tree(
    linear: ParseResults,
    mk_node: Type[UflBinaryNode] = ...
) -> UflNode: ...


def make_unary_operator_tree(
    linear: ParseResults,
    mk_node: Type[UflUnaryNode] = ...
) -> UflNode: ...
