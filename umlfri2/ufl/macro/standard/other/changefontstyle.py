from umlfri2.types.enums import FontStyle

from ....types.basic import UflBoolType
from ....types.complex import UflFontType
from ....types.enum import UflTypedEnumType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ....compilerhelpers.automultiresolver import resolve_multi_source


class ChangeFontStyleMacro(InlinedMacro):
    signature = MacroSignature(
        'change',
        UflFontType(),
        [UflTypedEnumType(FontStyle), UflBoolType()],
        UflFontType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        font_style = node.arguments[0].accept(visitor)
        value = node.arguments[1].accept(visitor)

        return resolve_multi_source(registrar, node.target.type, "({{0}}).change(({0}), ({1}))".format(font_style, value), target)
