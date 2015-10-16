from umlfri2.ufl.visitor.visitor import UflVisitor


class UflCompilingVisitor(UflVisitor):
    def __init__(self, params, enums):
        self.__params = params
        self.__enums = enums
    
    def get_function(self):
        pass
    
    def get_return_type(self):
        pass
    
    def visit_attribute_access(self, node):
        pass

    def visit_enum(self, node):
        pass

    def visit_method_call(self, node):
        pass

    def visit_variable(self, node):
        pass