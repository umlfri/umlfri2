from ....compilerhelpers.lambdainlining import LambdaInliningVisitor
from ....types.basic import UflBoolType
from ....types.generic import UflAnyType, UflGenericType
from ....types.structured import UflIterableType
from ....types.executable import UflLambdaType
from ...signature import MacroSignature
from ...inlined import InlinedMacro


class WhereMacro(InlinedMacro):
    src_type = UflGenericType(UflAnyType())
    
    signature = MacroSignature(
        'where',
        UflIterableType(src_type),
        [UflLambdaType([src_type], UflBoolType())],
        UflIterableType(src_type)
    )
    
    def compile(self, visitor, registrar, node):
        var = registrar.register_temp_variable()
        
        target = node.target.accept(visitor)
        inlining_visitor = LambdaInliningVisitor(var)
        inlined_condition_function = node.arguments[0].accept(inlining_visitor).accept(visitor)
        
        return "({0} for {0} in ({1}) if ({2}))".format(var, target, inlined_condition_function)
