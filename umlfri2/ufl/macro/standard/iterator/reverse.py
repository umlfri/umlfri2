from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class ReverseMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    macro_signature = MacroSignature('reverse', UflIterableType(src_type), [], UflIterableType(src_type))
    
    def compile(self, visitor, registrar, node):
        py_reversed = registrar.register_function(reversed)
        
        target = node.target.accept(visitor)
        
        return "{0}({1})".format(py_reversed, target)
