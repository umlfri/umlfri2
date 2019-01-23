from ....types.basic import UflStringType, UflBoolType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ...support.automultiresolver import resolve_multi


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

        return resolve_multi(registrar, node.target.type, "{0}(({{0}}).strip())".format(py_bool), target)
