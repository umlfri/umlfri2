from . import treecreator as treecreator
from ..tree import UflExpressionNode as UflExpressionNode, UflLambdaExpressionNode as UflLambdaExpressionNode, UflVariableDefinitionNode as UflVariableDefinitionNode, UflVariableNode as UflVariableNode
from .definition import WHOLE_EXPRESSION as WHOLE_EXPRESSION

from umlfri2.ufl.expressions.tree.expression import UflExpressionNode

def parse_ufl(expression: str) -> UflExpressionNode: ...
