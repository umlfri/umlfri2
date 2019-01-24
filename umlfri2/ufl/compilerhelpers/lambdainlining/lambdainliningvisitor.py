from .lambdainliningvisitorimpl import LambdaInliningVisitorImpl
from ...expressions.tree import UflTechnicalVariableNode
from ...expressions.tree.visitor import UflVisitor


class LambdaInliningVisitor(UflVisitor):
    def __init__(self, *variable_names):
        self.__variable_names = variable_names
    
    def visit_attribute_access(self, node):
        raise Exception
    
    def visit_enum(self, node):
        raise Exception
    
    def visit_macro_invoke(self, node):
        raise Exception
    
    def visit_technical_variable(self, node):
        raise Exception
    
    def visit_variable(self, node):
        raise Exception
    
    def visit_variable_definition(self, node):
        raise Exception("What happen here?")
    
    def visit_literal(self, node):
        raise Exception
    
    def visit_binary(self, node):
        raise Exception

    def visit_unary(self, node):
        raise Exception

    def visit_variable_metadata_access(self, node):
        raise Exception

    def visit_object_metadata_access(self, node):
        raise Exception

    def visit_unpack(self, node):
        raise Exception
    
    def visit_expression(self, node):
        raise Exception("What happen here?")
    
    def visit_lambda_expression(self, node):
        if node.parameter_count != len(self.__variable_names):
            raise Exception("Invalid inline: bad variable counts")
        
        if node.type is None:
            name_type = [(name, None) for name in node.parameters]
        else:
            name_type = [(name, type) for name, type in zip(node.parameters, node.type.parameter_types)]
        
        replacements = dict((var_name, UflTechnicalVariableNode(repl_name, var_type))
                                   for repl_name, (var_name, var_type) in zip(self.__variable_names, name_type))
        
        new_visitor = LambdaInliningVisitorImpl(replacements)
        return node.body.accept(new_visitor)
    
    def visit_cast(self, node):
        raise Exception
