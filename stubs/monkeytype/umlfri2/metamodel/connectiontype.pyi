from typing import (
    Any,
    List,
    Union,
)
from umlfri2.metamodel.connectiontypelabel import ConnectionTypeLabel
from umlfri2.metamodel.metamodel import Metamodel
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.image import Image
from umlfri2.ufl.components.connectionvisual.connectionvisualcontainer import (
    ConnectionVisualContainerComponent,
    ConnectionVisualContainerObject,
)
from umlfri2.ufl.context.typecontext import TypeContext
from umlfri2.ufl.types.structured.object import UflObjectType


class ConnectionType:
    def __init__(
        self,
        id: str,
        icon: Image,
        ufl_type: UflObjectType,
        appearance: ConnectionVisualContainerComponent,
        labels: List[Union[ConnectionTypeLabel, Any]]
    ) -> None: ...
    def _set_metamodel(self, metamodel: Metamodel) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def create_appearance_object(
        self,
        connection: ConnectionObject,
        ruler: QTRuler
    ) -> ConnectionVisualContainerObject: ...
    def get_label(self, id: str) -> ConnectionTypeLabel: ...
    @property
    def icon(self) -> Image: ...
    @property
    def id(self) -> str: ...
    @property
    def metamodel(self) -> Metamodel: ...
    @property
    def ufl_type(self) -> UflObjectType: ...
