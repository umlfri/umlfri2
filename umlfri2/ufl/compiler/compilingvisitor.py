from ..types import UflTypedEnumType, UflDataWithMetadataType, UflStringType, UflBoolType
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
        self.__variable_prefix = variable_prefix
    
    def visit_attribute_access(self, node):
        objcode = node.object.accept(self)
        
        if node.attribute in node.object.type.ALLOWED_DIRECT_ATTRIBUTES:
            return '{0}.{1}'.format(objcode, node.object.type.ALLOWED_DIRECT_ATTRIBUTES[node.attribute].accessor)
        
        return '{0}.get_value({1!r})'.format(objcode, node.attribute)
    
    def visit_enum(self, node):
        if isinstance(node.type, UflTypedEnumType):
            return "{0}.{1}".format(node.enum, node.item)
        else:
            return repr(node.item)
    
    def visit_method_call(self, node):
        targetcode = node.target.accept(self)
        
        params = [param.accept(self) for param in node.parameters]
        
        methoddesc = node.target.type.ALLOWED_DIRECT_METHODS[node.selector]
        
        return "({0}).{1}({2})".format(
            targetcode,
            methoddesc.selector,
            ", ".join("{0}".format(param) for param in params)
        )

    def visit_variable(self, node):
        var_name = node.name
        if self.__variable_prefix is not None:
            var_name = self.__variable_prefix + var_name
        
        return var_name
    
    def visit_binary(self, node):
        operand1 = node.operand1.accept(self)
        operand2 = node.operand2.accept(self)
        
        operator = self.__UFL_TO_PYTHON_OPERATOR.get(node.operator, node.operator)
        return '({0}) {1} ({2})'.format(operand1, operator, operand2)
    
    def visit_unary(self, node):
        operand = node.operand.accept(self)

        operator = self.__UFL_TO_PYTHON_OPERATOR.get(node.operator, node.operator)
        return "{0} ({1})".format(operator, operand)
    
    def visit_literal(self, node):
        return repr(node.value)
    
    def visit_metadata_access(self, node):
        return node.object.accept(self)
    
    def visit_iterator_access(self, node):
        raise NotImplementedError
    
    def visit_unpack(self, node):
        object = node.object.accept(self)
        return '({0}).{1}'.format(object, UflDataWithMetadataType.VALUE_ATTRIBUTE)
    
    def visit_expression(self, node):
        expression_source = node.result.accept(self)
        
        variables = (self.__variable_prefix + name for name in node.variables)
        
        return 'lambda {0}: {1}'.format(", ".join(variables), expression_source)
    
    def visit_cast(self, node):
        object = node.object.accept(self)
        
        if isinstance(node.type, UflStringType):
            return "str({0})".format(object)
        elif isinstance(node.type, UflBoolType):
            return "bool({0})".format(object)
        else:
            raise Exception
