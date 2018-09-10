from . import definition as d
from ..tree import *
from .operators import make_binary_operator_tree, make_unary_operator_tree


@d.VARIABLE_METADATA_ACCESS.setParseAction
def variable_metadata_access(data):
    return UflVariableMetadataAccessNode(UflVariableNode(data[1]))


@d.TARGET.setParseAction
def target(data):
    if len(data) > 1:
        return data[1]
    else:
        return data[0]


@d.VARIABLE.setParseAction
def variable(data):
    if data[0] == 'true':
        return UflLiteralNode(True)
    elif data[0] == 'false':
        return UflLiteralNode(False)
    elif data[0] == 'null':
        return UflLiteralNode(None)
    else:
        return UflVariableNode(data[0])


@d.NUMBER.setParseAction
def number(data):
    if '.' in data[0]:
        return UflLiteralNode(float(data[0]))
    else:
        return UflLiteralNode(int(data[0]))


@d.STRING.setParseAction
def string(data):
    return UflLiteralNode(data[0].strip("''"))


@d.UNARY.setParseAction
def unary(data):
    return make_unary_operator_tree(data, UflUnaryNode)


@d.BINARY.setParseAction
def binary(data):
    return make_binary_operator_tree(data, UflBinaryNode)


@d.ARGUMENTS.setParseAction
def arguments(data):
    return tuple(data[1:-1])


@d.METHOD_ATTRIBUTE_OR_ENUM.setParseAction
def method_attribute_or_enum(data):
    node = data[0]
    
    i = 1
    while i < len(data):
        if i + 2 < len(data) and isinstance(data[i + 2], tuple):
            if data[i] == '::':
                raise Exception('You can use :: operator only to access enum members')
            
            node = UflMacroInvokeNode(node, data[i + 1], data[i + 2], data[i] == '.')
            
            i += 3
        else:
            if data[i] == '->':
                raise Exception('Invalid use of iterator access operator')
            elif data[i] == '::':
                if isinstance(node, UflVariableNode):
                    node = UflEnumNode(node.name, data[i + 1])
                else:
                    raise Exception('You can use :: operator only to access enum members')
            else:
                node = UflAttributeAccessNode(node, data[i + 1])
            
            i += 2
    return node


@d.LAMBDA_EXPRESSION.setParseAction
def lambda_expression(data):
    return UflLambdaExpressionNode(data[-2], data[2:-3:2])
