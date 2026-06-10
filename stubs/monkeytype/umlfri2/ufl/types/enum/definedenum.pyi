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


class UflDefinedEnumType:
    def __init__(
        self,
        type: Union[Type[ArrowDefinition], Type[CornerDefinition], Type[SideDefinition]],
        possibilities: Dict[str, Union[CornerDefinition, ArrowDefinition, SideDefinition]] = ...,
        default: None = ...
    ) -> None: ...
    @property
    def type(
        self
    ) -> Union[Type[ArrowDefinition], Type[CornerDefinition], Type[SideDefinition]]: ...
