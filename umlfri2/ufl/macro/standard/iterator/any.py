from ....compilerhelpers.lambdainlining import LambdaInliningVisitor
from ....types.basic import UflBoolType
from ....types.generic import UflAnyType, UflAnyEquatableType, UflGenericType
from ....types.structured import UflIterableType, UflListType
from ....types.executable import UflLambdaType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class AnyMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'any',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflBoolType())],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        var = registrar.register_temp_variable()
        
        py_any = registrar.register_function(any)
        
        target = node.target.accept(visitor)
        
        inlining_visitor = LambdaInliningVisitor(var)
        inlined_condition_function = node.arguments[0].accept(inlining_visitor).accept(visitor)
        
        return "{0}(({1}) for {2} in ({3}))".format(py_any, inlined_condition_function, var, target)


class AnyContainsValueMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyEquatableType())
    
    signature = MacroSignature(
        'any',
        UflIterableType(src_type),
        [src_type],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        value = node.arguments[0].accept(visitor)
        
        return "({0}) in ({1})".format(value, target)


class AnyNotEmptyMacro(InlinedMacro):
    signature = MacroSignature(
        'any',
        UflIterableType(UflAnyType()),
        [],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        if isinstance(node.target.type, UflListType):
            return "({0}).get_length() > 0".format(target)
        else:
            py_any = registrar.register_function(any)
            
            return "{0}(True for _ in ({1}))".format(py_any, target)
