from weakref import ref


class Component:
    ATTRIBUTES = {}
    CHILDREN_ATTRIBUTES = {}
    HAS_CHILDREN = True
    CHILDREN_TYPE = None
    IS_CONTROL = False
    IS_HELPER = False
    SPECIAL_CHILDREN = {}
    ONLY_SPECIAL_CHILDREN = False
    
    def __init__(self, children):
        self.__children = children
        self.__parent = None
        
        for child in children:
            child.__parent = ref(self)
    
    def compile(self, type_context):
        pass
    
    def _change_attribute_type(self, attrname, type):
        self.ATTRIBUTES = {**self.ATTRIBUTES, attrname: type}
    
    def _compile_expressions(self, type_context, **expressions):
        for name, expression in expressions.items():
            expected_type = self.ATTRIBUTES[name]
            
            expression.compile(type_context, expected_type)
    
    def _compile_child_expressions(self, type_context, **expressions):
        for name, expression_dict in expressions.items():
            expected_type = self.CHILDREN_ATTRIBUTES[name]
            
            for expression in expression_dict.values():
                expression.compile(type_context, expected_type)
    
    def _compile_children(self, type_context):
        for child in self.__children:
            child.compile(type_context)
    
    def _get_children(self, context):
        for child in self.__children:
            if child.IS_CONTROL:
                yield from child.filter_children(context)
            else:
                yield context, child
    
    def _get_semantic_children(self):
        for child in self.__children:
            if child.IS_CONTROL:
                yield from child._get_semantic_children()
            else:
                yield child
    
    def _get_parent(self):
        return self.__parent()
