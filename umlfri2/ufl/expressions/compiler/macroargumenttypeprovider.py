from ..tree import UflUnpackNode, UflLambdaExpressionNode
from ...types import UflDataWithMetadataType
from ...types import UflLambdaType
from ...macro.argumenttypechecker import ArgumentTypeChecker


class MacroArgumentTypeProvider(ArgumentTypeChecker):
    def __init__(self, expressions, typing_visitor):
        self.__expressions = tuple(expressions)
        self.__typing_visitor = typing_visitor
        
        self.__typed_expressions = {}
    
    @property
    def argument_count(self):
        return len(self.__expressions)
    
    def check_argument(self, no, expected_type):
        expression = self.__expressions[no]
        
        if isinstance(expected_type, UflLambdaType):
            if not isinstance(expression, UflLambdaExpressionNode):
                return False
            
            if expected_type.parameter_count != expression.parameter_count:
                return False
            
            typed_expressions = self.__typed_expressions.setdefault(no, {})
            
            if expected_type not in typed_expressions:
                typed_arguments = {name: type for name, type in zip(expression.parameters, expected_type.parameter_types)}
                
                lambda_typing_visitor = self.__typing_visitor.create_for_lambda(typed_arguments)
                
                typed_body = expression.body.accept(lambda_typing_visitor)
                
                typed_expressions[expected_type] = UflLambdaExpressionNode(typed_body, expression.parameters, expected_type)
            
            return expected_type.return_type.is_assignable_from(typed_expressions[expected_type].body.type)
        else:
            if no not in self.__typed_expressions:
                node = self.__expressions[no].accept(self.__typing_visitor)
                
                while isinstance(node.type, UflDataWithMetadataType):
                    node = UflUnpackNode(node, node.type.underlying_type)
                
                self.__typed_expressions[no] = node
            
            return expected_type.is_assignable_from(self.__typed_expressions[no].type)
    
    def resolve_for(self, found_signature):
        for no, param_type in enumerate(found_signature.parameter_types):
            yield self.__typed_expressions[no]
