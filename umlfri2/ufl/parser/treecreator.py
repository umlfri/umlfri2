from . import definition as d
from ..tree import *
from .operators import make_binary_operator_tree, make_unary_operator_tree

d.METADATA_ACCESS.setParseAction(lambda data: UflMetadataAccessNode(data[1]))

def target(data):
    if len(data) > 1:
        return data[1]
    else:
        return data[0]

d.TARGET.setParseAction(target)

def variable(data):
    if data[0] == 'true':
        return UflLiteralNode(True)
    elif data[0] == 'false':
        return UflLiteralNode(False)
    elif data[0] == 'null':
        return UflLiteralNode(None)
    else:
        return UflVariableNode(data[0])

d.VARIABLE.setParseAction(variable)

def number(data):
    if '.' in data[0]:
        return UflLiteralNode(float(data[0]))
    else:
        return UflLiteralNode(int(data[0]))

d.NUMBER.setParseAction(number)

d.STRING.setParseAction(lambda data: UflLiteralNode(data[0].strip("''")))

d.UNARY.setParseAction(lambda data: make_unary_operator_tree(data, UflUnaryNode))

d.BINARY.setParseAction(lambda data: make_binary_operator_tree(data, UflBinaryNode))

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
                if data[i] == '->':
                    node = UflIteratorAccessNode(node, data[i + 1], data[i + 3: j: 2])
                else:
                    node = UflMethodCallNode(node, data[i + 1], data[i + 3: j: 2])
                i = j + 1
            else:
                if data[i] == '->':
                    raise Exception('Invalid use of iterator access operator')
                node = UflAttributeAccessNode(node, data[i + 1])
                i = i + 2
        return node

d.METHODORATTRORENUM.setParseAction(method_or_attribute_or_enum)
