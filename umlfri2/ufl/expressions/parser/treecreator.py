from . import definition as d
from ..tree import *
from .operators import make_binary_operator_tree, make_unary_operator_tree


@d.METADATA_ACCESS.setParseAction
def metadata_access(data):
    return UflMetadataAccessNode(data[1])


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


@d.METHODORATTRORENUM.setParseAction
def method_or_attribute_or_enum(data):
    node = data[0]
    
    if len(data) > 1 and data[1] == '::':
        if isinstance(data[0], UflVariableNode):
            return UflEnumNode(data[0].name, data[2])
        else:
            raise Exception('You can use :: operator only to access enum members')
    else:
        i = 1
        while i < len(data):
            if i + 2 < len(data) and data[i + 2] == '(':
                j = i + 2
                while data[j] != ')':
                    j += 1
                
                node = UflMacroInvokeNode(node, data[i + 1], data[i + 3: j: 2], data[i] == '.')
                
                i = j + 1
            else:
                if data[i] == '->':
                    raise Exception('Invalid use of iterator access operator')
                
                node = UflAttributeAccessNode(node, data[i + 1])
                
                i = i + 2
        return node
