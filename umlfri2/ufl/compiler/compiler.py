from .typingvisitor import UflTypingVisitor
from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl


def compile_ufl(expression, expected_type, variables, variable_prefix=None, enums={}):
    tree = parse_ufl(expression)
    
    typing_visitor = UflTypingVisitor(variables, enums, variable_prefix, expected_type)
    typed_tree = tree.accept(typing_visitor)
    
    visitor = UflCompilingVisitor(variable_prefix)
    code = typed_tree.accept(visitor)
    
    lambda_code = 'lambda {0}: {1}'.format(", ".join(variables.keys()), code)
    
    return typed_tree.type, eval(lambda_code, enums.copy())
