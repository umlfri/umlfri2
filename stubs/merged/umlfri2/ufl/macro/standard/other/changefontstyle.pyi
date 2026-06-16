from ....compilerhelpers.automultiresolver import resolve_multi_source as resolve_multi_source
from ....types.basic import UflBoolType as UflBoolType
from ....types.complex import UflFontType as UflFontType
from ....types.enum import UflTypedEnumType as UflTypedEnumType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete
from umlfri2.types.enums import FontStyle as FontStyle

class ChangeFontStyleMacro(InlinedMacro):
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
