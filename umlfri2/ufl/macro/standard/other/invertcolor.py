from ....types.complex import UflColorType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ....compilerhelpers.automultiresolver import resolve_multi_source


class InvertColorMacro(InlinedMacro):
    signature = MacroSignature(
        'invert',
        UflColorType(),
        [],
        UflColorType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        return resolve_multi_source(registrar, node.target.type, "({0}).invert()", target)
