from ..types.enum import UflFlagsType as UflFlagsType
from ..types.structured import UflIterableType as UflIterableType, UflListType as UflListType, UflNullableType as UflNullableType
from _typeshed import Incomplete
from typing import NamedTuple

class MultiType(NamedTuple):
    type: Incomplete
    is_multi_invoke: Incomplete
    is_null_invoke: Incomplete

def resolve_multi_source(registrar, target_type, src_format, target): ...
def resolve_multi_type(target_type): ...
