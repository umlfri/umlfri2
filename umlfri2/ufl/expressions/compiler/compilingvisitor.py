import math

from umlfri2.types.color import Colors
from umlfri2.types.enums import ALL_ENUMS
from umlfri2.types.font import Fonts

from .varnameregister import VariableNameRegister
from ...macro.inlined import InlinedMacro
from ...types.enum import UflTypedEnumType
from ...types.structured import UflVariableWithMetadataType
from ...types.complex import UflColorType, UflFontType
from ...types.basic import UflStringType, UflBoolType
from ..tree.visitor import UflVisitor


class UflCompilingVisitor(UflVisitor):
    """
    Compiles UflExpression into python code
    """
    
    __UFL_TO_PYTHON_OPERATOR = {
        '&&': 'and',
        '||': 'or',
        '!': 'not',
    }
    
    def __init__(self, variable_prefix):
        self.__name_register = VariableNameRegister(variable_prefix)
        
        self.__variable_prefix = variable_prefix
    
    def visit_attribute_access(self, node):
        objcode = node.object.accept(self)
        
        if node.attribute in node.object.type.ALLOWED_DIRECT_ATTRIBUTES:
            return '{0}.{1}'.format(objcode, node.object.type.ALLOWED_DIRECT_ATTRIBUTES[node.attribute].accessor)
        
        return '{0}.get_value({1!r})'.format(objcode, node.attribute)
    
    def visit_enum(self, node):
        if isinstance(node.type, UflTypedEnumType):
            py_enum = self.__name_register.register_class(ALL_ENUMS[node.enum])
            return "{0}.{1}".format(py_enum, node.item)
        elif isinstance(node.type, UflColorType):
            py_colors = self.__name_register.register_class(Colors)
            return "{0}.{1}".format(py_colors, node.item)
        elif isinstance(node.type, UflFontType):
            py_fonts = self.__name_register.register_class(Fonts)
            return "{0}.{1}".format(py_fonts, node.item)
        else:
            return repr(node.item)
    
    def visit_macro_invoke(self, node):
        if isinstance(node.macro, InlinedMacro):
            return node.macro.compile(self, self.__name_register, node)
        else:
            raise Exception("I can not use non-inline macro yet")
    
    def visit_variable(self, node):
        return self.__fix_var_name(node.name)
    
    def visit_variable_definition(self, node):
        return self.__fix_var_name(node.name)
    
    def visit_binary(self, node):
        operand1 = node.operand1.accept(self)
        operand2 = node.operand2.accept(self)
        
        if node.operator == '/':
            py_division = self.__name_register.register_function(self.__division)
            return "{0}({1}, {2})".format(py_division, operand1, operand2)
        elif node.operator == '//':
            py_true_division = self.__name_register.register_function(self.__true_division)
            return "{0}({1}, {2})".format(py_true_division, operand1, operand2)
        else:
            operator = self.__UFL_TO_PYTHON_OPERATOR.get(node.operator, node.operator)
            return '({0}) {1} ({2})'.format(operand1, operator, operand2)
    
    @staticmethod
    def __division(a, b):
        if b:
            return a/b
        elif a < 0:
            return -math.inf
        elif a:
            return math.inf
        else:
            return math.nan
    
    @staticmethod
    def __true_division(a, b):
        if b:
            return int(a//b)
        elif a < 0:
            return -math.inf
        elif a:
            return math.inf
        else:
            return math.nan
    
    def visit_unary(self, node):
        operand = node.operand.accept(self)

        operator = self.__UFL_TO_PYTHON_OPERATOR.get(node.operator, node.operator)
        return "{0} ({1})".format(operator, operand)
    
    def visit_literal(self, node):
        return repr(node.value)
    
    def visit_variable_metadata_access(self, node):
        return node.object.accept(self)
    
    def visit_object_metadata_access(self, node):
        objcode = node.object.accept(self)
        metadata_type = node.object.type.metadata_type

        return '{0}.{1}'.format(objcode, metadata_type.ALLOWED_DIRECT_ATTRIBUTES[node.metadata_name].accessor)
    
    def visit_unpack(self, node):
        object = node.object.accept(self)
        return '({0}).{1}'.format(object, UflVariableWithMetadataType.VALUE_ATTRIBUTE)
    
    def visit_expression(self, node):
        expression_source = node.result.accept(self)
        
        variables = ", ".join(var.accept(self) for var in node.variables)
        
        return 'lambda {0}: {1}'.format(variables, expression_source)
    
    def visit_lambda_expression(self, node):
        body_source = node.body.accept(self)

        parameters = ", ".join(self.__fix_var_name(param) for param in node.parameters)
        
        return 'lambda {0}: ({1})'.format(parameters, body_source)
    
    def visit_cast(self, node):
        object = node.object.accept(self)
        
        if isinstance(node.type, UflStringType):
            py_str = self.__name_register.register_function(str)
            return "{0}({1})".format(py_str, object)
        elif isinstance(node.type, UflBoolType):
            py_bool = self.__name_register.register_function(bool)
            return "{0}({1})".format(py_bool, object)
        else:
            raise Exception
    
    def __fix_var_name(self, name):
        if self.__variable_prefix is None:
            return name
        else:
            return self.__variable_prefix + name
    
    @property
    def all_globals(self):
        return self.__name_register.build_globals()
