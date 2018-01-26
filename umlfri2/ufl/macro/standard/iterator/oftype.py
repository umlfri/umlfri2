from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class OfTypeMacro(InlinedMacro):
    base_type = UflGenericType(UflAnyType())
    dest_type = UflGenericType(base_type)
    
    macro_signature = MacroSignature(
        'of_type',
        UflIterableType(base_type),
        [UflTypeIdentifierType(dest_type)],
        UflIterableType(dest_type)
    )
    
    def compile(self, visitor, registrar, node):
        raise NotImplementedError
