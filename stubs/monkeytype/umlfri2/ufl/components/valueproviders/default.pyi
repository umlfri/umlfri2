from typing import (
    Optional,
    Union,
)
from umlfri2.types.enums.arroworientation import ArrowOrientation
from umlfri2.types.enums.lineorientation import LineOrientation
from umlfri2.types.proportion import Proportion
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.basic.integer import UflIntegerType
from umlfri2.ufl.types.complex.proportion import UflProportionType
from umlfri2.ufl.types.enum.typedenum import UflTypedEnumType
from umlfri2.ufl.types.structured.nullable import UflNullableType


class DefaultValueProvider:
    def __call__(
        self,
        context: Context
    ) -> Optional[Union[ArrowOrientation, Proportion, int, LineOrientation]]: ...
    def __init__(
        self,
        value: Optional[Union[ArrowOrientation, Proportion, int, LineOrientation]]
    ) -> None: ...
    def compile(
        self,
        type_context: TypeContext,
        expected_type: Union[UflNullableType, UflProportionType, UflIntegerType, UflTypedEnumType]
    ) -> None: ...
