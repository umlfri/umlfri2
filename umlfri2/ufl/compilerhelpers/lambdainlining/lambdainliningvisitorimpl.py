from ...expressions.tree import *
from ...expressions.tree.visitor import UflVisitor


class LambdaInliningVisitorImpl(UflVisitor):
    def __init__(self, replacements):
        self.__replacements = replacements
    
    def visit_attribute_access(self, node):
        obj = node.object.accept(self)
        return UflAttributeAccessNode(obj, node.attribute, node.type)
    
    def visit_enum(self, node):
        return node
    
    def visit_macro_invoke(self, node):
        target = node.target.accept(self)
        arguments = [arg.accept(self) for arg in node.arguments]
        
        return UflMacroInvokeNode(target, node.selector, arguments,
                                  node.inner_type_invoke, node.macro, node.type)
    
    def visit_technical_variable(self, node):
        return node
    
    def visit_variable(self, node):
        if node.name in self.__replacements:
            return self.__replacements[node.name]
        return node
    
    def visit_variable_definition(self, node):
        raise Exception("What happen here?")
    
    def visit_literal(self, node):
        return node
    
    def visit_binary(self, node):
        operand1 = node.operand1.accept(self)
        operand2 = node.operand2.accept(self)
        
        return UflBinaryNode(operand1, node.operator, operand2, node.type)

    def visit_unary(self, node):
        operand = node.operand.accept(self)
        
        return UflUnaryNode(node.operator, operand, node.type)

    def visit_variable_metadata_access(self, node):
        object = node.object.accept(self)
        
        return UflVariableMetadataAccessNode(object, node.type)

    def visit_object_metadata_access(self, node):
        object = node.object.accept(self)
        
        return UflObjectMetadataAccessNode(object, node.metadata_name, node.type)

    def visit_unpack(self, node):
        object = node.object.accept(self)
        
        return UflUnpackNode(object, node.type)
    
    def visit_expression(self, node):
        raise Exception("What happen here?")
    
    def visit_lambda_expression(self, node):
        new_replacements = self.__replacements.copy()
        
        for param in node.parameters:
            del new_replacements[param]
        
        if not new_replacements:
            return node
        
        new_visitor = LambdaInliningVisitorImpl(new_replacements)
        body = node.body.accept(new_visitor)
        
        return UflLambdaExpressionNode(body, node.parameters, node.type)
    
    def visit_cast(self, node):
        object = node.object.accept(self)
        
        return UflCastNode(object, node.type)
