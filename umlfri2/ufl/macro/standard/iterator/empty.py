from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class EmptyMacro(InlinedMacro):
    signature = MacroSignature(
        'empty',
        UflIterableType(UflAnyType()),
        [],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        if isinstance(node.target.type, UflListType):
            return "({0}).get_length() == 0".format(target)
        else:
            py_any = registrar.register_function(any)
            
            return "not {0}(True for _ in ({1}))".format(py_any, target)
