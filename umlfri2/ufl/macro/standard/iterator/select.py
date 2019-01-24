from ....compilerhelpers.lambdainlining import LambdaInliningVisitor
from ....types.generic import UflAnyType, UflGenericType
from ....types.structured import UflIterableType
from ....types.executable import UflLambdaType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class SelectMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    dest_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'select',
        UflIterableType(src_type),
        [UflLambdaType([src_type], dest_type)],
        UflIterableType(dest_type)
    )
    
    def compile(self, visitor, registrar, node):
        var = registrar.register_temp_variable()
    
        target = node.target.accept(visitor)
        inlining_visitor = LambdaInliningVisitor(var)
        inlined_collection_function = node.arguments[0].accept(inlining_visitor).accept(visitor)
    
        return "(({0}) for {1} in ({2}))".format(inlined_collection_function, var, target)
