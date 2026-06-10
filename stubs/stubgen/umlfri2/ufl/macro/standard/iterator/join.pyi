from ....types.basic import UflStringType as UflStringType
from ....types.structured import UflIterableType as UflIterableType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class JoinMacro(InlinedMacro):
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
