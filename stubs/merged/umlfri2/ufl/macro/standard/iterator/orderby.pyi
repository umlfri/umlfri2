from ....types.enum import UflTypedEnumType as UflTypedEnumType
from ....types.executable import UflLambdaType as UflLambdaType
from ....types.generic import UflAnyComparableType as UflAnyComparableType, UflAnyType as UflAnyType, UflGenericType as UflGenericType
from ....types.structured import UflIterableType as UflIterableType
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete
from umlfri2.types.enums import Order as Order

class OrderByMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...

class OrderByOrderMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
