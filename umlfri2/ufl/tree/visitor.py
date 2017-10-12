import abc


class UflVisitor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def visit_attribute_access(self, node):
        pass
    
    @abc.abstractmethod
    def visit_enum(self, node):
        pass
    
    @abc.abstractmethod
    def visit_method_call(self, node):
        pass
    
    @abc.abstractmethod
    def visit_variable(self, node):
        pass
    
    @abc.abstractmethod
    def visit_literal(self, node):
        pass
    
    @abc.abstractmethod
    def visit_binary(self, node):
        pass

    @abc.abstractmethod
    def visit_metadata_access(self, node):
        pass
