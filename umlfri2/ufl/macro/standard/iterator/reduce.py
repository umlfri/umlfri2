import functools

from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class ReduceMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    value_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'reduce',
        UflIterableType(src_type),
        [value_type, UflLambdaType([value_type, src_type], value_type)],
        value_type
    )
    
    def compile(self, visitor, registrar, node):
        py_reduce = registrar.register_function(functools.reduce)
        
        target = node.target.accept(visitor)
        initial_value = node.arguments[0].accept(visitor)
        reduce_function = node.arguments[1].accept(visitor)
        
        return "{0}(({1}), ({2}), ({3}))".format(py_reduce, reduce_function, target, initial_value)


class ReduceSimpleMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'reduce',
        UflIterableType(src_type),
        [UflLambdaType([src_type, src_type], src_type)],
        src_type
    )
    
    def compile(self, visitor, registrar, node):
        py_reduce = registrar.register_function(functools.reduce)
        
        target = node.target.accept(visitor)
        reduce_function = node.arguments[0].accept(visitor)
        
        return "{0}(({1}), ({2}))".format(py_reduce, reduce_function, target)
