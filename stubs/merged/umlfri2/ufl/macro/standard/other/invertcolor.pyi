from ....compilerhelpers.automultiresolver import resolve_multi_source as resolve_multi_source
from ....types.complex import UflColorType as UflColorType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class InvertColorMacro(InlinedMacro):
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
