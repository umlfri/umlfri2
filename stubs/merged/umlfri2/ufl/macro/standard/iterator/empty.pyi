from ....types.basic import UflBoolType as UflBoolType
from ....types.generic import UflAnyType as UflAnyType
from ....types.structured import UflIterableType as UflIterableType, UflListType as UflListType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class EmptyMacro(InlinedMacro):
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
