from ..types import UflTypedEnumType, UflObjectType
from .visitor import UflVisitor


class UflCompilingVisitor(UflVisitor):
    """
    Compiles UflExpression into python code
    """
    def __init__(self, params, enums):
        self.__params = params
        self.__enums = enums
    
    def visit_attribute_access(self, node):
        objtype, objcode = node.object.accept(self)
        
        if node.attribute in objtype.ALLOWED_DIRECT_ATTRIBUTES:
            attrname, attrtype = objtype.ALLOWED_DIRECT_ATTRIBUTES[node.attribute]
            return attrtype, '{0}.{1}'.format(objcode, attrname)
        
        if isinstance(objtype, UflObjectType) and objtype.contains_attribute(node.attribute):
            return objtype.get_attribute_type(node.attribute), '{0}[{1!r}]'.format(objcode, node.attribute)
        
        raise Exception("Unknown attribute {0}".format(node.attribute))

    def visit_enum(self, node):
        enum = self.__enums[node.enum]
        
        if node.item not in enum.possibilities:
            raise Exception("Unknown enum item {0}::{1}".format(node.enum, node.item))
        
        if isinstance(enum, UflTypedEnumType):
            return enum, "{0}.{1}".format(enum.name, node.item)
        else:
            return enum, repr(node.item)
            

    def visit_method_call(self, node):
        targettype, targetcode = node.target.accept(self)
        
        paramtypes = []
        params = []
        
        for param in node.parameters:
            type, code = param.accept(self)
            paramtypes.append(type)
            params.append(code)
        
        if not node.selector in targettype.ALLOWED_DIRECT_METHODS:
            raise Exception("Unknown method {0}".format(node.selector))
        
        methoddesc = targettype.ALLOWED_DIRECT_METHODS[node.selector]
        if tuple(paramtypes) != methoddesc.parameters:
            raise Exception("Incorrect param types")
        
        return methoddesc.return_type, "{0}.{1}({2})".format(
            targetcode,
            methoddesc.selector,
            ", ".join("({0})".format(i) for i in params)
        )

    def visit_variable(self, node):
        return self.__params[node.name], node.name
