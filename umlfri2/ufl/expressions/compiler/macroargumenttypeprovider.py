from ..tree import UflUnpackNode
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
        if isinstance(expected_type, UflLambdaType):
            return False
        else:
            if no not in self.__typed_expressions:
                self.__typed_expressions[no] = self.__demeta_argument(self.__expressions[no].accept(self.__typing_visitor))
            
            return expected_type.is_assignable_from(self.__typed_expressions[no].type)
    
    def __demeta_argument(self, node):
        while isinstance(node.type, UflDataWithMetadataType):
            node = UflUnpackNode(node, node.type.underlying_type)
        return node
    
    def resolve_for(self, found_signature):
        for no, param_type in enumerate(found_signature.parameter_types):
            yield self.__typed_expressions[no]
