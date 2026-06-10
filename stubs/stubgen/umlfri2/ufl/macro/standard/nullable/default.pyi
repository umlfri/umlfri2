from ....types.generic import UflAnyType as UflAnyType, UflAnyWithDefault as UflAnyWithDefault, UflGenericType as UflGenericType
from ....types.structured import UflNullableType as UflNullableType
from ....uniquevaluegenerator import UniqueValueGenerator as UniqueValueGenerator
from ...inlined import InlinedMacro as InlinedMacro
from ...signature import MacroSignature as MacroSignature
from _typeshed import Incomplete

class DefaultUniqueValueGenerator(UniqueValueGenerator):
    def get_parent_name(self): ...
    def has_value(self, value): ...
    def for_name(self, name): ...

class DefaultMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...

class DefaultWithValueMacro(InlinedMacro):
    src_type: Incomplete
    signature: Incomplete
    def compile(self, visitor, registrar, node): ...
