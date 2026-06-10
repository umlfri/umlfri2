from umlfri2.metamodel.connectiontype import ConnectionType
from umlfri2.model.connection.connectionobject import ConnectionObject
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.proportion import Proportion
from umlfri2.ufl.components.visual.visualcontainer import (
    VisualContainerComponent,
    VisualObjectContainer,
)
from umlfri2.ufl.context.typecontext import TypeContext


class ConnectionTypeLabel:
    def __init__(
        self,
        position: Proportion,
        id: str,
        appearance: VisualContainerComponent
    ) -> None: ...
    def _set_connection_type(self, connection_type: ConnectionType) -> None: ...
    def compile(self, type_context: TypeContext) -> None: ...
    def create_appearance_object(
        self,
        connection: ConnectionObject,
        ruler: QTRuler
    ) -> VisualObjectContainer: ...
    @property
    def id(self) -> str: ...
    @property
    def position(self) -> Proportion: ...
