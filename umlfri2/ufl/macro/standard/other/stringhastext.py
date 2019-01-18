from ....types.basic import UflStringType, UflBoolType
from ....types.structured import UflIterableType, UflListType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class StringHasTextMacro(InlinedMacro):
    signature = MacroSignature(
        'has_text',
        UflStringType(),
        [],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        py_bool = registrar.register_function(bool)
        
        if isinstance(node.target.type, (UflIterableType, UflListType)):
            var = registrar.register_temp_variable()
            
            return "({0}(({1}).strip()) for {1} in ({2}))".format(py_bool, var, target)
        else:
            return "{0}(({1}).strip())".format(py_bool, target)
