from . import definition as d

from ..tree import *

def target(data):
    if len(data) > 1:
        return data[1]
    else:
        return data[0]

d.TARGET.addParseAction(target)

d.VARIABLE.addParseAction(lambda data: UflVariable(data[0]))

def method_or_attribute_or_enum(data):
    node = data[0]
    
    if len(data) > 1 and data[1] == '::':
        return UflEnum(data[0], data[2])
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
