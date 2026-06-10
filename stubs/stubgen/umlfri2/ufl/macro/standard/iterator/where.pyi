from ....compilerhelpers.lambdainlining import LambdaInliningVisitor as LambdaInliningVisitor
from ....types.basic import UflBoolType as UflBoolType
from ....types.executable import UflLambdaType as UflLambdaType
from ....types.generic import UflAnyType as UflAnyType, UflGenericType as UflGenericType
from ....types.structured import UflIterableType as UflIterableType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class WhereMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
