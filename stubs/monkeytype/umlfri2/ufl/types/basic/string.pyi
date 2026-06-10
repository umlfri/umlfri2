from typing import (
    Optional,
    Tuple,
    Union,
)
from umlfri2.model.diagram import DiagramValueGenerator
from umlfri2.model.element.elementobject import ElementValueGenerator
from umlfri2.ufl.components.text.textcontainer import TextContainerComponent
from umlfri2.ufl.objects.mutable.list import ListItemValueGenerator


class UflStringType:
    def __init__(
        self,
        possibilities: Optional[Tuple[str, str, str, str, str, str, str, str]] = ...,
        default: None = ...,
        template: Optional[TextContainerComponent] = ...,
        multiline: bool = ...
    ) -> None: ...
    def build_default(
        self,
        generator: Optional[Union[ElementValueGenerator, ListItemValueGenerator, DiagramValueGenerator]]
    ) -> str: ...
    def is_default_value(self, value: str) -> bool: ...
    @property
    def is_immutable(self) -> bool: ...
    def is_valid_value(self, value: str) -> bool: ...
    @property
    def multiline(self) -> bool: ...
    def parse(self, value: str) -> str: ...
    @property
    def possibilities(self) -> Optional[Tuple[str, str, str, str, str, str, str, str]]: ...
