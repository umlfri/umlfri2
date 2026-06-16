from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionShownEvent as ConnectionShownEvent
from umlfri2.application.events.model import ConnectionCreatedEvent as ConnectionCreatedEvent
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


class AddDiagramConnectionCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        connection_type: ConnectionType,
        source_element: ElementVisual,
        destination_element: ElementVisual,
        points: List[Union[Any, Point]]
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def connection_visual(self) -> ConnectionVisual: ...
    @property
    def connection_object(self): ...
    def get_updates(
        self
    ) -> Iterator[Union[ConnectionCreatedEvent, ConnectionShownEvent]]: ...
