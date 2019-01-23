from ....types.complex import UflColorType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ...support.automultiresolver import resolve_multi


class InvertColorMacro(InlinedMacro):
    signature = MacroSignature(
        'invert',
        UflColorType(),
        [],
        UflColorType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        return resolve_multi(registrar, node.target.type, "({0}).invert()", target)
