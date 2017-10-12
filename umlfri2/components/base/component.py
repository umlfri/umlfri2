from weakref import ref


class Component:
    ATTRIBUTES = {}
    CHILDREN_ATTRIBUTES = {}
    HAS_CHILDREN = True
    CHILDREN_TYPE = None
    IS_CONTROL = False
    
    def __init__(self, children):
        self.__children = children
        self.__parent = None
        
        for child in children:
            child.__parent = ref(self)
    
    def compile(self, type_context):
        pass
    
    def _compile_expressions(self, type_context, **expressions):
        for name, expression in expressions.items():
            expected_type = self.ATTRIBUTES[name]
            
            expression.compile(type_context, expected_type)
            
            actual_type = expression.get_type()
            if not expected_type.is_same_as(actual_type):
                raise Exception("Invalid type for attribute {0} ({1}, but {2} expected)".format(name, actual_type, expected_type))
    
    def _compile_children(self, type_context):
        for child in self.__children:
            child.compile(type_context)
    
    def _get_children(self, context):
        for child in self.__children:
            if child.IS_CONTROL:
                yield from child.filter_children(context)
            else:
                yield context, child
    
    def _get_parent(self):
        return self.__parent()
