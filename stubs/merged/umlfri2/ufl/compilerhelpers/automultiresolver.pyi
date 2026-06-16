from ..types.enum import UflFlagsType as UflFlagsType
from ..types.structured import UflIterableType as UflIterableType, UflListType as UflListType, UflNullableType as UflNullableType
from _typeshed import Incomplete
from typing import NamedTuple

from typing import Union
from umlfri2.ufl.expressions.compiler.varnameregister import VariableNameRegister
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.structured.list import UflListType
from umlfri2.ufl.types.structured.object import UflObjectType
from umlfri2.ufl.types.structured.variablemetadata import UflVariableMetadataType

class MultiType(NamedTuple):
    type: Incomplete
    is_multi_invoke: Incomplete
    is_null_invoke: Incomplete

def resolve_multi_source(
    registrar: VariableNameRegister,
    target_type: Union[UflStringType, UflVariableMetadataType, UflFontType, UflObjectType],
    src_format: str,
    target: str
) -> str: ...
def resolve_multi_type(
    target_type: Union[UflObjectType, UflStringType, UflFontType, UflListType, UflVariableMetadataType]
) -> MultiType: ...
