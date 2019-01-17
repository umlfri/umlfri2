from ....types.generic import UflAnyType, UflGenericType
from ....types.structured import UflNullableType, UflIterableType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class IterateMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'iterate',
        UflNullableType(src_type),
        [],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        py_iterate = registrar.register(self.__iterate)
        
        target = node.target.accept(visitor)
        
        return "{0}({1})".format(py_iterate, target)
    
    @staticmethod
    def __iterate(nullable):
        if nullable is not None:
            yield nullable
