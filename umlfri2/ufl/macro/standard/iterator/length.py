from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class LengthMacro(InlinedMacro):
    signature = MacroSignature(
        'length',
        UflIterableType(UflAnyType()),
        [],
        UflIntegerType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        if isinstance(node.target.type, UflListType):
            return "({0}).get_length()".format(target)
        else:
            py_sum = registrar.register_function(sum)
            
            return "{0}(1 for _ in ({0}))".format(py_sum, target)
