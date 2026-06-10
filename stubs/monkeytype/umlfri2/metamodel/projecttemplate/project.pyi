from typing import (
    Any,
    Iterator,
    List,
    Union,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.metamodel.projecttemplate.diagram import DiagramTemplate
from umlfri2.metamodel.projecttemplate.element import ElementTemplate
from umlfri2.types.image import Image


class ProjectTemplate:
    def __init__(
        self,
        id: str,
        elements: List[Union[Any, ElementTemplate]],
        connections: List[Any],
        diagrams: List[Union[Any, DiagramTemplate]]
    ) -> None: ...
    def _set_metamodel(self, metamodel: Metamodel) -> None: ...
    @property
    def addon(self) -> AddOn: ...
    def compile(self) -> None: ...
    @property
    def connections(self) -> None: ...
    @property
    def diagrams(self) -> Iterator[DiagramTemplate]: ...
    @property
    def elements(self) -> Iterator[ElementTemplate]: ...
    @property
    def icon(self) -> Image: ...
    @property
    def id(self) -> str: ...
    @property
    def metamodel(self) -> Metamodel: ...
