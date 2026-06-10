from ....types.generic import UflAnyType as UflAnyType, UflGenericType as UflGenericType, UflTypeIdentifierType as UflTypeIdentifierType
from ....types.structured import UflIterableType as UflIterableType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class OfTypeMacro(InlinedMacro):
    base_type: Incomplete
    dest_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node) -> None: ...
