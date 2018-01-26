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
        
        if isinstance(node.target.type, (UflIterableType, UflListType)):
            var = registrar.register_temp_variable()
            
            return "({0}.invert() for {0} in ({1}))".format(var, target)
        else:
            return "({0}).invert()".format(target)
