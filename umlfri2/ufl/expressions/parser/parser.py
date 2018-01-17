# noinspection PyUnresolvedReferences
from . import treecreator
from .definition import WHOLE_EXPRESSION
from ..tree import UflExpressionNode, UflVariableNode, UflVariableDefinitionNode


def parse_ufl(expression):
    result = WHOLE_EXPRESSION.parseString(expression)[0]
    
    # find all used variable names
    variable_names = {var.name for var in result.find(lambda node: isinstance(node, UflVariableNode))}
    
    if 'self' in variable_names:
        variable_names.remove('self')
        
        variables = (
            UflVariableDefinitionNode('self'),
            *(UflVariableDefinitionNode(name) for name in variable_names)
        )
    else:
        variables = tuple(UflVariableDefinitionNode(name) for name in variable_names)
    
    return UflExpressionNode(result, variables)
