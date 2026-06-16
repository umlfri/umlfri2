from _typeshed import Incomplete
from enum import Enum
from typing import NamedTuple

from pyparsing.results import ParseResults
from typing import (
    Optional,
    Type,
)
from umlfri2.ufl.expressions.tree.binary import UflBinaryNode
from umlfri2.ufl.expressions.tree.node import UflNode
from umlfri2.ufl.expressions.tree.unary import UflUnaryNode

class PriorityGroup(Enum):
    Unary = 1
    Power = 2
    Multiplicative = 3
    Additive = 4
    Relational = 5
    LogicalAdditive = 6
    LogicalMultiplicative = 7

BINARY_PRIORITIES: Incomplete
BINARY_OPERATOR_SYNONYMS: Incomplete
BINARY_OPERATORS: Incomplete
UNARY_OPERATOR_LIST: Incomplete
UNARY_OPERATOR_SYNONYMS: Incomplete
UNARY_OPERATORS: Incomplete
OPERATOR_KEYWORDS: Incomplete

def get_priority(operator: str) -> int: ...
def get_binary_operator(operator: Optional[str]) -> Optional[str]: ...
def get_unary_operator(operator: str) -> str: ...

class operator_tree_stack_node(NamedTuple):
    value: Incomplete
    operator: Incomplete

def make_binary_operator_tree(
    linear: ParseResults,
    mk_node: Type[UflBinaryNode] = ...
) -> UflNode: ...
def make_unary_operator_tree(
    linear: ParseResults,
    mk_node: Type[UflUnaryNode] = ...
) -> UflNode: ...
