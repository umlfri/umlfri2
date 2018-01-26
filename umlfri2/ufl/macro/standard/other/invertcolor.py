from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class InvertColorMacro(InlinedMacro):
    signature = MacroSignature(
        'invert',
        UflColorType(),
        [],
        UflColorType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        return "({0}).invert()".format(target)
