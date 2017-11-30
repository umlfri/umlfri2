from . import definition as d
from pyparsing import ParseException
from ..tree import *


d.METADATA_ACCESS.addParseAction(lambda data: UflMetadataAccess(data[1]))

def target(data):
    if len(data) > 1:
        return data[1]
    else:
        return data[0]

d.TARGET.addParseAction(target)

def variable(data):
    if data[0] == 'true':
        return UflLiteral(True)
    elif data[0] == 'false':
        return UflLiteral(False)
    elif data[0] == 'null':
        return UflLiteral(None)
    else:
        return UflVariable(data[0])

d.VARIABLE.addParseAction(variable)

def number(data):
    if '.' in data[0]:
        return UflLiteral(float(data[0]))
    else:
        return UflLiteral(int(data[0]))

d.NUMBER.addParseAction(number)

d.STRING.addParseAction(lambda data: UflLiteral(data[0].strip("''")))

def unary(data):
    x = data[:]
    value = x.pop(-1)
    
    while x:
        operator = x.pop(-1)
        value = UflUnary(operator, value)
    
    return value

d.UNARY.setParseAction(unary)

def binary(data):
    if len(data) > 2:
        return UflBinary(data[0], data[1], data[2])
    else:
        return data[0]

d.BINARY.addParseAction(binary)

def method_or_attribute_or_enum(data):
    node = data[0]
    
    if len(data) > 1 and data[1] == '::':
        if isinstance(data[0], UflVariable):
            return UflEnum(data[0].name, data[2])
        else:
            raise ParseException('You can use :: operator only to access enum members')
    else:
        i = 1
        while i < len(data):
            if i + 2 < len(data) and data[i + 2] == '(':
                j = i + 2
                while data[j] != ')':
                    j += 1
                node = UflMethodCall(node, data[i + 1], data[i + 3 : j : 2])
                i = j + 1
            else:
                node = UflAttributeAccess(node, data[i + 1])
                i = i + 2
        return node

d.METHODORATTRORENUM.addParseAction(method_or_attribute_or_enum)
