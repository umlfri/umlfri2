from .enum import UflEnumType as UflEnumType
from .enumpossibility import UflEnumPossibility as UflEnumPossibility

from typing import (
    Dict,
    Optional,
    Type,
    Union,
)
from umlfri2.ufl.components.connectionvisual.arrow import ArrowDefinition
from umlfri2.ufl.components.visual.rectangle import (
    CornerDefinition,
    SideDefinition,
)

class UflDefinedEnumType(UflEnumType):
    def __init__(
        self,
        type: Union[Type[ArrowDefinition], Type[CornerDefinition], Type[SideDefinition]],
        possibilities: Dict[str, Union[CornerDefinition, ArrowDefinition, SideDefinition]] = ...,
        default: None = ...
    ) -> None: ...
    @property
    def name(self): ...
    @property
    def type(
        self
    ) -> Union[Type[ArrowDefinition], Type[CornerDefinition], Type[SideDefinition]]: ...
    def is_assignable_from(self, other): ...
    def is_equatable_to(self, other): ...
