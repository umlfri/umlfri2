class UflVisitor:
    def visit_attribute_access(self, node):
        raise NotImplementedError
    
    def visit_enum(self, node):
        raise NotImplementedError
    
    def visit_macro_invoke(self, node):
        raise NotImplementedError
    
    def visit_technical_variable(self, node):
        raise NotImplementedError
    
    def visit_variable(self, node):
        raise NotImplementedError
    
    def visit_variable_definition(self, node):
        raise NotImplementedError
    
    def visit_literal(self, node):
        raise NotImplementedError
    
    def visit_binary(self, node):
        raise NotImplementedError
    
    def visit_unary(self, node):
        raise NotImplementedError
    
    def visit_variable_metadata_access(self, node):
        raise NotImplementedError

    def visit_object_metadata_access(self, node):
        raise NotImplementedError

    def visit_unpack(self, node):
        raise NotImplementedError
    
    def visit_expression(self, node):
        raise NotImplementedError

    def visit_lambda_expression(self, node):
        raise NotImplementedError
    
    def visit_cast(self, node):
        raise NotImplementedError
