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
        
        font_style = node.arguments[0].accept(visitor)
        value = node.arguments[1].accept(visitor)
        
        if isinstance(node.target.type, (UflIterableType, UflListType)):
            var = registrar.register_temp_variable()
            
            return "({0}.change(({1}), ({2})) for {0} in ({3}))".format(var, font_style, value, target)
        else:
            return "({0}).change(({1}), ({2}))".format(target, font_style, value)
