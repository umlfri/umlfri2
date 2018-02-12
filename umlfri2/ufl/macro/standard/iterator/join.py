from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class JoinMacro(InlinedMacro):
    signature = MacroSignature(
        'join',
        UflIterableType(UflStringType()),
        [UflStringType()],
        UflStringType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        separator = node.arguments[0].accept(visitor)
        
        return "({0}).join({1})".format(separator, target)
