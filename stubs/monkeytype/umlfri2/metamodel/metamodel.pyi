from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Union,
)
from umlfri2.application.addon.local.addon import AddOn
from umlfri2.metamodel.connectiontype import ConnectionType
from umlfri2.metamodel.diagramtype import DiagramType
from umlfri2.metamodel.elementtype import ElementType
from umlfri2.metamodel.projecttemplate.project import ProjectTemplate
from umlfri2.metamodel.translation.translation import Translation
from umlfri2.ufl.components.connectionvisual.arrow import ArrowDefinition
from umlfri2.ufl.components.visual.rectangle import (
    CornerDefinition,
    SideDefinition,
)
from umlfri2.ufl.types.structured.object import UflObjectType


class Metamodel:
    def __init__(
        self,
        diagrams: Dict[str, DiagramType],
        elements: Dict[str, ElementType],
        connections: Dict[str, ConnectionType],
        templates: List[ProjectTemplate],
        definitions: Dict[str, Union[Dict[str, ArrowDefinition], Dict[str, CornerDefinition], Dict[str, SideDefinition]]],
        translations: List[Union[Translation, Any]],
        config: Optional[UflObjectType]
    ) -> None: ...
    def _set_addon(self, addon: AddOn) -> None: ...
    @property
    def addon(self) -> AddOn: ...
    def compile(self) -> None: ...
    @property
    def config_structure(self) -> UflObjectType: ...
    @property
    def diagram_types(self) -> Iterator[DiagramType]: ...
    @property
    def element_types(self) -> Iterator[ElementType]: ...
    def get_connection_type(self, name: str) -> ConnectionType: ...
    def get_diagram_type(self, name: str) -> DiagramType: ...
    def get_element_type(self, name: str) -> ElementType: ...
    def get_translation(self, language: str) -> Translation: ...
    @property
    def has_config(self) -> bool: ...
    @property
    def templates(self) -> Iterator[ProjectTemplate]: ...
