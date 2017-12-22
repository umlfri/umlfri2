# noinspection PyUnresolvedReferences
from . import treecreator
from .definition import WHOLE_EXPRESSION
from ..tree import UflExpressionNode


def parse_ufl(expression):
    return UflExpressionNode(WHOLE_EXPRESSION.parseString(expression)[0])
