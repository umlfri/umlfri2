from umlfri2.types.enums import Order

from ....types.enum import UflTypedEnumType
from ....types.generic import UflAnyType, UflAnyComparableType, UflGenericType
from ....types.structured import UflIterableType
from ....types.executable import UflLambdaType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class OrderByMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'order_by',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflAnyComparableType())],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_sorted = registrar.register_function(sorted)
        
        target = node.target.accept(visitor)
        key_function = node.arguments[0].accept(visitor)
        
        return "{0}(({1}), key=({2}))".format(py_sorted, target, key_function)


class OrderByOrderMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'order_by',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflAnyComparableType()), UflTypedEnumType(Order)],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_sorted = registrar.register_function(sorted)
        
        target = node.target.accept(visitor)
        key_function = node.arguments[0].accept(visitor)
        order = node.arguments[1].accept(visitor)
        
        return "{0}(({1}), key=({2}), reverse=({3}) == Order.desc)".format(py_sorted, target, key_function, order)
