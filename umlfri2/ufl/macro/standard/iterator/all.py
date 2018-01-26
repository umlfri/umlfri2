from ....types import *
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class AllMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'all',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflBoolType())],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        var = registrar.register_temp_variable()
        
        py_all = registrar.register_function(all)
        
        target = node.target.accept(visitor)
        
        inlined_condition_function = node.parameters[0].inline(var).accept(visitor)
        
        return "{0}(({1}) for {2} in ({3}))".format(py_all, inlined_condition_function, var, target)
