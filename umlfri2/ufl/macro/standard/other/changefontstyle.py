from umlfri2.types.enums import FontStyle

from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class ChangeFontStyleMacro(InlinedMacro):
    signature = MacroSignature(
        'change',
        UflFontType(),
        [UflTypedEnumType(FontStyle), UflBoolType()],
        UflFontType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        font_style = node.parameters[0].accept(visitor)
        value = node.parameters[1].accept(visitor)
        
        return "({0}).change(({1}), ({2}))".format(target, font_style, value)
