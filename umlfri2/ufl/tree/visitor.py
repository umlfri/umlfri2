class UflVisitor:
    def visit_attribute_access(self, node):
        raise NotImplementedError
    
    def visit_enum(self, node):
        raise NotImplementedError
    
    def visit_method_call(self, node):
        raise NotImplementedError
    
    def visit_variable(self, node):
        raise NotImplementedError
    
    def visit_literal(self, node):
        raise NotImplementedError
    
    def visit_binary(self, node):
        raise NotImplementedError
    
    def visit_unary(self, node):
        raise NotImplementedError
    
    def visit_metadata_access(self, node):
        raise NotImplementedError

    def visit_iterator_access(self, node):
        raise NotImplementedError
