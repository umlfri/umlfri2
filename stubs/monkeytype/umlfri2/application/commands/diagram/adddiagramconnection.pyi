from typing import (
    Any,
    Iterator,
    List,
    Union,
)
from umlfri2.application.events.diagram.connectionshown import ConnectionShownEvent
from umlfri2.application.events.model.connectioncreated import ConnectionCreatedEvent
from umlfri2.metamodel.connectiontype import ConnectionType
from umlfri2.model.connection.connectionvisual import ConnectionVisual
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler
from umlfri2.types.geometry.point import Point


class AddDiagramConnectionCommand:
    def __init__(
        self,
        diagram: Diagram,
        connection_type: ConnectionType,
        source_element: ElementVisual,
        destination_element: ElementVisual,
        points: List[Union[Any, Point]]
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    @property
    def connection_visual(self) -> ConnectionVisual: ...
    def get_updates(
        self
    ) -> Iterator[Union[ConnectionCreatedEvent, ConnectionShownEvent]]: ...
