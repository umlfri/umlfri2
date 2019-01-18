from ..tree import UflUnpackNode, UflLambdaExpressionNode
from ...types.structured import UflVariableWithMetadataType
from ...types.executable import UflLambdaType
from ...macro.argumenttypechecker import ArgumentTypeChecker, ArgumentTypeCheckerResult


class MacroArgumentTypeProvider(ArgumentTypeChecker):
    def __init__(self, target_type, expressions, typing_visitor):
        self.__target_type = target_type
        
        self.__expressions = tuple(expressions)
        self.__typing_visitor = typing_visitor
        
        self.__typed_expressions = {}
    
    def check_arguments(self, self_type, expected_types, return_type):
        generic_cache = {}
        
        resolved_self_type = self_type.resolve_generic(self.__target_type, generic_cache)
        if resolved_self_type is None:
            return None
        
        expected_types = tuple(expected_types)
        
        if len(expected_types) != len(self.__expressions):
            return None
        
        typed_node_list = []
        for macro_parameter_node, macro_parameter_type in zip(self.__expressions, expected_types):
            typed_node = self.__resolve_argument(macro_parameter_node, macro_parameter_type, generic_cache)
            if typed_node is None:
                return None
            typed_node_list.append(typed_node)
        
        self.__typed_expressions[expected_types] = typed_node_list
        
        resolved_return_type = return_type.resolve_unknown_generic(generic_cache)
        if resolved_return_type is None:
            return None
        
        return ArgumentTypeCheckerResult([node.type for node in typed_node_list], resolved_return_type)
    
    def __resolve_argument(self, expression, expected_type, generic_cache):
        if isinstance(expression, UflLambdaExpressionNode):
            if not isinstance(expected_type, UflLambdaType):
                return None
            
            if expected_type.parameter_count != expression.parameter_count:
                return None
            
            typed_arguments = {}
            resolved_param_types = []
            for name, type in zip(expression.parameters, expected_type.parameter_types):
                resolved_type = type.resolve_unknown_generic(generic_cache)
                if resolved_type is None:
                    return None
                typed_arguments[name] = resolved_type
                resolved_param_types.append(resolved_type)
            
            lambda_typing_visitor = self.__typing_visitor.create_for_lambda(typed_arguments)
            typed_body = expression.body.accept(lambda_typing_visitor)
            
            return_type = expected_type.return_type.resolve_generic(typed_body.type, generic_cache)
            if return_type is None:
                return None
            return UflLambdaExpressionNode(typed_body, expression.parameters, UflLambdaType(resolved_param_types, return_type))
        else:
            node = expression.accept(self.__typing_visitor)
            
            while isinstance(node.type, UflVariableWithMetadataType):
                node = UflUnpackNode(node, node.type.underlying_type)
                
            resolved_type = expected_type.resolve_generic(node.type, generic_cache)
            if resolved_type is None:
                return None
            return node
    
    def resolve_for(self, found_signature):
        yield from self.__typed_expressions[found_signature.parameter_types]
