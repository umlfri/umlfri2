from ....types.generic import UflAnyType as UflAnyType, UflGenericType as UflGenericType
from ....types.structured import UflIterableType as UflIterableType, UflNullableType as UflNullableType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class IterateMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
