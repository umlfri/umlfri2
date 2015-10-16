from umlfri2.ufl.types import UflTypedEnumType, UflNullableType


class Component:
    ATTRIBUTES = {}
    HAS_CHILDREN = True
    
    def __init__(self, children):
        self.__children = children
        self.__parent = None
        
        for child in children:
            child.__parent = self
    
    def is_control(self):
        raise NotImplementedError
    
    def compile(self, variables):
        pass
    
    def _compile_expressions(self, variables, **expressions):
        for name, expression in expressions.items():
            expression.compile(variables)
            
            expected_metatype = self.ATTRIBUTES[name]
            actual_type = expression.get_type()
            
            wrong_type = False
            
            if isinstance(expected_metatype, UflNullableType):
                if actual_type is None:
                    continue
                expected_metatype = expected_metatype.inner_type
            
            if isinstance(expected_metatype, UflTypedEnumType):
                if not isinstance(actual_type, UflTypedEnumType):
                    raise Exception("Invalid type for attribute {0} ({1}, but {2} expected)".format(name, actual_type, expected_metatype))
                elif expected_metatype.type is not actual_type.type:
                    raise Exception("Invalid type for attribute {0} ({1}, but {2} expected)".format(name, actual_type, expected_metatype))
            elif not isinstance(actual_type, expected_metatype):
                raise Exception("Invalid type for attribute {0} ({1}, but {2} expected)".format(name, actual_type, expected_metatype.__name__))
    
    def _compile_children(self, variables):
        for child in self.__children:
            child.compile(variables)
    
    def _get_children(self, context):
        for child in self.__children:
            if child.is_control():
                yield from child.filter_children(context)
            else:
                yield context, child
    
    def _get_parent(self):
        return self.__parent
