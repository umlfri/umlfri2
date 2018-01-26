from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class DefaultMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'default',
        UflNullableType(src_type),
        [],
        src_type
    )
    
    def compile(self, visitor, registrar, node):
        raise NotImplementedError


class DefaultWithValueMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'default',
        UflNullableType(src_type),
        [src_type],
        src_type
    )
    
    def compile(self, visitor, registrar, node):
        py_iterate = registrar.register(self.__default)
        
        target = node.target.accept(visitor)
        
        default_value = node.parameters[0].accept(visitor)
        
        return "{0}(({1}), ({2}))".format(py_iterate, target, default_value)
    
    @staticmethod
    def __default(nullable, default):
        if nullable is None:
            return default
        else:
            return nullable
