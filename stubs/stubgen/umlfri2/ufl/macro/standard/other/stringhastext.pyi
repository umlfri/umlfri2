from ....compilerhelpers.automultiresolver import resolve_multi_source as resolve_multi_source
from ....types.basic import UflBoolType as UflBoolType, UflStringType as UflStringType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class StringHasTextMacro(InlinedMacro):
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
