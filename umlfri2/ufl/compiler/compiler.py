from .typingvisitor import UflTypingVisitor
from .compilingvisitor import UflCompilingVisitor
from ..parser import parse_ufl
from umlfri2.ufl.types import UflBoolType, UflStringType, UflDataWithMetadataType


def compile_ufl(expression, expected_type, variables, variable_prefix=None, enums={}):
    tree = parse_ufl(expression)
    
    typing_visitor = UflTypingVisitor(variables, enums, variable_prefix)
    typed_tree = tree.accept(typing_visitor)
    
    visitor = UflCompilingVisitor(variable_prefix)
    code = typed_tree.accept(visitor)
    
    return_type = typed_tree.type
    if not isinstance(expected_type, UflDataWithMetadataType) and isinstance(return_type, UflDataWithMetadataType):
        code = '({0}).{1}'.format(code, UflDataWithMetadataType.VALUE_ATTRIBUTE)
        return_type = return_type.underlying_type
    
    if isinstance(expected_type, UflBoolType) and not isinstance(return_type, UflBoolType):
        code = "bool({0})".format(code)
        return_type = UflBoolType()
    if isinstance(expected_type, UflStringType) and not isinstance(return_type, UflStringType) and return_type.is_convertable_to_string:
        code = "str({0})".format(code)
        return_type = UflStringType()
    
    code = 'lambda {0}: {1}'.format(", ".join(variables.keys()), code)
    
    return return_type, eval(code, enums.copy())
