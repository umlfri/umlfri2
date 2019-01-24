from ....types.basic import UflStringType, UflBoolType
from ...signature import MacroSignature
from ...inlined import InlinedMacro
from ....compilerhelpers.automultiresolver import resolve_multi_source


class StringEmptyMacro(InlinedMacro):
    signature = MacroSignature(
        'empty',
        UflStringType(),
        [],
        UflBoolType()
    )
    
    def compile(self, visitor, registrar, node):
        target = node.target.accept(visitor)
        
        py_bool = registrar.register_function(bool)

        return resolve_multi_source(registrar, node.target.type, "not {0}(({{0}}).strip())".format(py_bool), target)
