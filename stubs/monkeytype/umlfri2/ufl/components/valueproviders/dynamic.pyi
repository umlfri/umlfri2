from typing import (
    Optional,
    Union,
)
from umlfri2.types.color import Color
from umlfri2.types.font import Font
from umlfri2.ufl.components.valueproviders.valuesourceposition import ValueSourcePosition
from umlfri2.ufl.context.context import Context
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.objects.immutable.list import UflList
from umlfri2.ufl.types.base.type import UflType
from umlfri2.ufl.types.enum.stringenum import UflStringEnumType
from umlfri2.ufl.types.structured.iterable import UflIterableType
from umlfri2.ufl.types.structured.list import UflListType


class DynamicValueProvider:
    def __call__(
        self,
        context: Context
    ) -> Union[Font, Color, str, UflList, bool]: ...
    def __init__(
        self,
        expression: str,
        source: Optional[ValueSourcePosition] = ...
    ) -> None: ...
    def compile(
        self,
        type_context: TypeContext,
        expected_type: UflType
    ) -> None: ...
    def get_type(
        self
    ) -> Union[UflIterableType, UflListType, UflStringEnumType]: ...
