from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl


def compile_ufl(expression, variables, enums = {}):
    visitor = UflCompilingVisitor(variables, enums)
    tree = parse_ufl(expression)
    
    return_type, code = tree.accept(visitor)
    
    code = 'lambda {0}: {1}'.format(", ".join(variables.keys()), code)
    
    return return_type, eval(code, enums)
