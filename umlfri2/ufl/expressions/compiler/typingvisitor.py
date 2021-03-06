from umlfri2.types.color import Colors
from umlfri2.types.enums import ALL_ENUMS
from umlfri2.types.font import Fonts

from ...compilerhelpers.automultiresolver import resolve_multi_type
from ...macro.standard import STANDARD_MACROS
from ...types.structured import UflVariableWithMetadataType, UflNullableType, UflObjectType, UflIterableType
from ...types.basic import UflDecimalType, UflNumberType, UflBoolType, UflStringType, UflIntegerType
from ...types.enum import UflTypedEnumType
from ...types.complex import UflColorType, UflFontType

from ..tree.visitor import UflVisitor
from ..tree import *

from .macroargumenttypeprovider import MacroArgumentTypeProvider


class UflTypingVisitor(UflVisitor):
    """
    Type checks UflExpression into python code
    """
    
    def __init__(self, params, expected_type):
        self.__params = params
        self.__enums = {name: UflTypedEnumType(enum) for name, enum in ALL_ENUMS.items()}
        self.__expected_type = expected_type
    
    def visit_attribute_access(self, node):
        obj = self.__demeta(node.object.accept(self))
        obj_type, multi_invoke, null_invoke = resolve_multi_type(obj.type)
        
        if node.attribute in obj_type.ALLOWED_DIRECT_ATTRIBUTES:
            attr_type = obj_type.ALLOWED_DIRECT_ATTRIBUTES[node.attribute].type
        elif isinstance(obj_type, UflObjectType) and obj_type.contains_attribute(node.attribute):
            attr_type = obj_type.get_attribute(node.attribute).type
        else:
            raise Exception("Unknown attribute {0}".format(node.attribute))
        
        if multi_invoke:
            attr_type = UflIterableType(attr_type)
        elif null_invoke and not isinstance(attr_type, UflNullableType):
            attr_type = UflNullableType(attr_type)
        
        return UflAttributeAccessNode(obj, node.attribute, attr_type)
    
    def visit_enum(self, node):
        if node.enum == 'Color':
            if not Colors.exists(node.item):
                raise Exception("Unknown enum item {0}::{1}".format(node.enum, node.item))
            
            return UflEnumNode(node.enum, node.item, UflColorType())
        elif node.enum == 'Font':
            if not Fonts.exists(node.item):
                raise Exception("Unknown enum item {0}::{1}".format(node.enum, node.item))
            
            return UflEnumNode(node.enum, node.item, UflFontType())
        else:
            enum_type = self.__enums[node.enum]
            
            if not enum_type.is_valid_item(node.item):
                raise Exception("Unknown enum item {0}::{1}".format(node.enum, node.item))
            
            return UflEnumNode(node.enum, node.item, enum_type)
    
    def visit_macro_invoke(self, node):
        target = self.__demeta(node.target.accept(self))

        target_type, multi_invoke, null_invoke = resolve_multi_type(target.type)
        if not node.inner_type_invoke:
            target_type = target.type
            if not multi_invoke and not null_invoke:
                raise Exception("Iterator access operator cannot be applied to the type {0}".format(target_type))
            multi_invoke = False
            null_invoke = False
        
        params = MacroArgumentTypeProvider(target_type, node.arguments, self)
        
        found_macro, found_signature = self.__find_macro(node.selector, params)
        
        return_type = found_signature.true_result_type
        
        if multi_invoke:
            return_type = UflIterableType(return_type)
        elif null_invoke:
            return_type = UflNullableType(return_type)
        
        return UflMacroInvokeNode(target, node.selector, params.resolve_for(found_signature), node.inner_type_invoke,
                                  found_macro, return_type)
    
    def visit_technical_variable(self, node):
        raise Exception("Something weird happen. Cannot type technical variable")
    
    def visit_variable(self, node):
        return UflVariableNode(node.name, self.__params[node.name])
    
    def visit_variable_definition(self, node):
        return UflVariableDefinitionNode(node.name, self.__params[node.name])
    
    def visit_binary(self, node):
        operand1 = self.__demeta(node.operand1.accept(self))
        operand2 = self.__demeta(node.operand2.accept(self))
        
        if node.operator in ('!=', '=='):
            if not (operand1.type.is_equatable_to(operand2.type) or operand2.type.is_equatable_to(operand1.type)):
                raise Exception("Incompatible types {0} and {1}".format(operand1.type, operand2.type))
            
            type = UflBoolType()
        elif node.operator in ('<', '>', '<=', '>='):
            if not (operand1.type.is_comparable_with(operand2.type) or operand2.type.is_comparable_with(operand1.type)):
                raise Exception("Incompatible types {0} and {1}".format(operand1.type, operand2.type))
            
            type = UflBoolType()
        elif node.operator in ('+', '-', '*', '/', '//', '%'):
            if not isinstance(operand1.type, UflNumberType) or not isinstance(operand2.type, UflNumberType):
                raise Exception("Cannot apply arithmetic operator to {0} and {1}".format(operand1.type, operand2.type))
            
            if node.operator == '//':
                type = UflIntegerType()
            elif isinstance(operand1.type, UflDecimalType) or isinstance(operand2.type, UflDecimalType):
                type = UflDecimalType()
            else:
                type = UflIntegerType()
        elif node.operator in ('||', '&&'):
            if not isinstance(operand1.type, UflBoolType) or not isinstance(operand2.type, UflBoolType):
                raise Exception("Cannot apply logic operator to {0} and {1}".format(operand1.type, operand2.type))
            
            if node.operator == '&&':
                type = UflBoolType()
            else:
                type = UflBoolType()
        else:
            raise Exception
        
        return UflBinaryNode(operand1, node.operator, operand2, type)
    
    def visit_unary(self, node):
        operand = self.__demeta(node.operand.accept(self))
        
        if node.operator == '!':
            if not isinstance(operand.type, UflBoolType):
                raise Exception("Cannot apply operator ! to anything but boolean value")
            type = UflBoolType()
        elif node.operator in ('+', '-'):
            if isinstance(operand.type, UflDecimalType):
                type = UflDecimalType()
            elif isinstance(operand.type, UflIntegerType):
                type = UflIntegerType()
            else:
                raise Exception("Cannot apply arithmetic operator to anything but number")
        else:
            raise Exception
        
        return UflUnaryNode(node.operator, operand, type)
    
    def visit_literal(self, node):
        if isinstance(node.value, str):
            type = UflStringType()
        elif isinstance(node.value, bool):
            type = UflBoolType()
        elif isinstance(node.value, int):
            type = UflIntegerType()
        elif isinstance(node.value, float):
            type = UflDecimalType()
        elif node.value is None:
            type = UflNullableType(None)
        else:
            raise Exception('Invalid literal')
        
        return UflLiteralNode(node.value, type)
    
    def visit_variable_metadata_access(self, node):
        object = node.object.accept(self)
        if not isinstance(object.type, UflVariableWithMetadataType):
            raise Exception('Does not have metadata for the value, cannot apply metadata access operator')

        return UflVariableMetadataAccessNode(object, object.type.metadata_type)

    def visit_object_metadata_access(self, node):
        object = node.object.accept(self)
        if not isinstance(object.type, UflVariableWithMetadataType):
            raise Exception('Does not have metadata for the object, cannot apply object metadata access operator')
        
        metadata_type = object.type.metadata_type
        
        if node.metadata_name not in metadata_type.ALLOWED_DIRECT_ATTRIBUTES:
            raise Exception('Does not have metadata "{0}" for the object'.format(node.metadata_name))
        
        attr_type = metadata_type.ALLOWED_DIRECT_ATTRIBUTES[node.metadata_name].type
        
        return UflObjectMetadataAccessNode(object, node.metadata_name, attr_type)

    def visit_unpack(self, node):
        raise Exception("Weird ufl expression tree")
    
    def visit_expression(self, node):
        ret = self.__demeta(node.result.accept(self))
        
        variables = tuple(var.accept(self) for var in node.variables)
        
        if not self.__expected_type.is_assignable_from(ret.type) and ret.type.is_convertible_to(self.__expected_type):
            ret = UflCastNode(ret, self.__expected_type)
        
        return UflExpressionNode(ret, variables, ret.type)
    
    def visit_lambda_expression(self, node):
        raise Exception("Lambda expression used in invalid context")
    
    def visit_cast(self, node):
        raise Exception("Weird ufl expression tree")
    
    def __demeta(self, node):
        while isinstance(node.type, UflVariableWithMetadataType):
            node = UflUnpackNode(node, node.type.underlying_type)
        return node
    
    def create_for_lambda(self, lambda_args):
        return UflTypingVisitor({**self.__params, **lambda_args}, None)
    
    def __find_macro(self, selector, argument_types):
        for macro in STANDARD_MACROS:
            found_signature = macro.compare_signature(selector, argument_types)
            if found_signature is not None:
                return macro, found_signature
        
        raise Exception("Unknown macro {0}".format(selector))
