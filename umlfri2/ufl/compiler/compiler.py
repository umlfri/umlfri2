from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl
from umlfri2.ufl.types import UflBoolType, UflStringType


def compile_ufl(expression, expected_type, variables, enums = {}):
    visitor = UflCompilingVisitor(variables, enums)
    tree = parse_ufl(expression)
    
    return_type, code = tree.accept(visitor)
    
    if isinstance(expected_type, UflBoolType) and not isinstance(return_type, UflBoolType):
        code = "bool({0})".format(code)
        return_type = UflBoolType()
    if isinstance(expected_type, UflStringType) and not isinstance(return_type, UflStringType):
        code = "str({0})".format(code)
        return_type = UflStringType()
    
    code = 'lambda {0}: {1}'.format(", ".join(variables.keys()), code)
    
    return return_type, eval(code, enums)
