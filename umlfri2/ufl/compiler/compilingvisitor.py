from umlfri2.ufl.types import UflDataWithMetadataType, UflNullableType, UflAnyType
from ..types import UflTypedEnumType, UflObjectType, UflBoolType, UflStringType, UflIntegerType
from ..tree.visitor import UflVisitor


class UflCompilingVisitor(UflVisitor):
    """
    Compiles UflExpression into python code
    """
    def __init__(self, params, enums, variable_prefix):
        self.__params = params
        self.__enums = {name: UflTypedEnumType(enum) for name, enum in enums.items()}
        self.__variable_prefix = variable_prefix
    
    def visit_attribute_access(self, node):
        objtype, objcode = self.__demeta(node.object.accept(self))
        
        if node.attribute in objtype.ALLOWED_DIRECT_ATTRIBUTES:
            attrname, attrtype = objtype.ALLOWED_DIRECT_ATTRIBUTES[node.attribute]
            return attrtype, '{0}.{1}'.format(objcode, attrname)
        
        if isinstance(objtype, UflObjectType) and objtype.contains_attribute(node.attribute):
            return objtype.get_attribute(node.attribute).type, '{0}.get_value({1!r})'.format(objcode, node.attribute)
        
        raise Exception("Unknown attribute {0}".format(node.attribute))

    def visit_enum(self, node):
        enum = self.__enums[node.enum]
        
        if not enum.is_valid_item(node.item):
            raise Exception("Unknown enum item {0}::{1}".format(node.enum, node.item))
        
        if isinstance(enum, UflTypedEnumType):
            return enum, "{0}.{1}".format(enum.name, node.item)
        else:
            return enum, repr(node.item)
            

    def visit_method_call(self, node):
        targettype, targetcode = self.__demeta(node.target.accept(self))
        
        paramtypes = []
        params = []
        
        for param in node.parameters:
            type, code = param.accept(self)
            paramtypes.append(type)
            params.append(code)
        
        if not node.selector in targettype.ALLOWED_DIRECT_METHODS:
            raise Exception("Unknown method {0}".format(node.selector))
        
        methoddesc = targettype.ALLOWED_DIRECT_METHODS[node.selector]
        if len(paramtypes) != len(methoddesc.parameters):
            raise Exception("Incorrect param count")
        
        for actual, expected in zip(paramtypes, methoddesc.parameters):
            if not actual.is_same_as(expected):
                raise Exception("Incorrect param types")
        
        return methoddesc.return_type, "{0}.{1}({2})".format(
            targetcode,
            methoddesc.selector,
            ", ".join("({0})".format(i) for i in params)
        )

    def visit_variable(self, node):
        var_name = node.name
        if self.__variable_prefix is not None:
            var_name = self.__variable_prefix + var_name
        
        return self.__params[var_name], var_name
    
    def visit_binary(self, node):
        ltype, lvalue = self.__demeta(node.operand1.accept(self))
        rtype, rvalue = self.__demeta(node.operand2.accept(self))
        
        if ltype.is_same_as(rtype):
            raise Exception("Incompatible types {0} and {1}".format(ltype, rtype))
        
        if node.operator in ('<', '>', '<=', '>=', '!=', '=='):
             return UflBoolType(), lvalue + node.operator + rvalue
    
    def visit_unary(self, node):
        type, value = self.__demeta(node.operand.accept(self))
        
        if node.operator == '!':
            if not isinstance(type, UflBoolType):
                raise Exception("Cannot apply operator ! to anything but boolean value")
            return UflBoolType(), "not ({0})".format(value)
    
    def visit_literal(self, node):
        if isinstance(node.value, str):
            return UflStringType(), repr(node.value)
        elif isinstance(node.value, bool):
            return UflBoolType(), repr(node.value)
        elif isinstance(node.value, int):
            return UflIntegerType(), repr(node.value)
        elif node.value is None:
            return UflNullableType(UflAnyType()), 'None'
        else:
            raise Exception('Invalid literal')
    
    def visit_metadata_access(self, node):
        type, object = node.object.accept(self)
        if not isinstance(type, UflDataWithMetadataType):
            raise Exception('Does not have metadata for the value, cannot apply metadata access operator')
        
        return type.metadata_type, object
    
    def __demeta(self, type_and_value):
        if isinstance(type_and_value[0], UflDataWithMetadataType):
            return type_and_value[0].underlying_type, '({0}).value'.format(type_and_value[1])
        return type_and_value
