# noinspection PyUnresolvedReferences
from . import treecreator
from .definition import WHOLE_EXPRESSION

def parse_ufl(expression):
    return WHOLE_EXPRESSION.parseString(expression)[0]
