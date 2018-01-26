from umlfri2.types.enums import Order

from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class OrderByMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    # TODO: UflAnyType must be comparable
    signature = MacroSignature(
        'order_by',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflAnyType())],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_sorted = registrar.register_function(sorted)
        
        target = node.target.accept(visitor)
        key_function = node.parameters[0].accept(visitor)
        
        return "{0}(({1}), key=({2}))".format(py_sorted, target, key_function)


class OrderByOrderMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    # TODO: UflAnyType must be comparable
    signature = MacroSignature(
        'order_by',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflAnyType()), UflTypedEnumType(Order)],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_sorted = registrar.register_function(sorted)
        
        target = node.target.accept(visitor)
        key_function = node.parameters[0].accept(visitor)
        order = node.parameters[1].accept(visitor)
        
        return "{0}(({1}), key=({2}), reverse=({3}) == Order.desc)".format(py_sorted, target, key_function, order)
