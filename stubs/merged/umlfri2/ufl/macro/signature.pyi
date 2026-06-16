from _typeshed import Incomplete
from typing import NamedTuple

from typing import (
    Any,
    List,
    Optional,
    Union,
)
from umlfri2.ufl.expressions.compiler.macroargumenttypeprovider import MacroArgumentTypeProvider
from umlfri2.ufl.types.base.type import UflType
from umlfri2.ufl.types.basic.string import UflStringType
from umlfri2.ufl.types.complex.color import UflColorType
from umlfri2.ufl.types.complex.font import UflFontType
from umlfri2.ufl.types.structured.iterable import UflIterableType
from umlfri2.ufl.types.structured.nullable import UflNullableType

class FoundSignature(NamedTuple):
    self_type: Incomplete
    parameter_types: Incomplete
    return_type: Incomplete
    true_argument_types: Incomplete
    true_result_type: Incomplete

class MacroSignature:
    def __init__(
        self,
        identifier: str,
        self_type: Union[UflStringType, UflNullableType, UflIterableType, UflFontType, UflColorType],
        parameter_types: List[Any],
        return_type: UflType
    ) -> None: ...
    def compare(
        self,
        selector: str,
        argument_type_checker: MacroArgumentTypeProvider
    ) -> Optional[FoundSignature]: ...
