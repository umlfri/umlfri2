from ..base import Command as Command
from _typeshed import Incomplete
from collections.abc import Generator
from umlfri2.application.events.diagram import ConnectionShownEvent as ConnectionShownEvent, ElementShownEvent as ElementShownEvent
from umlfri2.application.events.model import ConnectionCreatedEvent as ConnectionCreatedEvent, ElementCreatedEvent as ElementCreatedEvent
from umlfri2.model.element import ElementVisual as ElementVisual
from typing import (
    Iterator,
    Union,
)
from umlfri2.application.events.diagram.connectionshown import ConnectionShownEvent
from umlfri2.application.events.diagram.elementshown import ElementShownEvent
from umlfri2.application.events.model.connectioncreated import ConnectionCreatedEvent
from umlfri2.application.events.model.elementcreated import ElementCreatedEvent
from umlfri2.application.snippet.snippet import Snippet
from umlfri2.model.diagram import Diagram
from umlfri2.model.element.elementvisual import ElementVisual
from umlfri2.qtgui.rendering.qtruler import QTRuler


class DuplicateSnippetCommand(Command):
    def __init__(
        self,
        diagram: Diagram,
        snippet: Snippet
    ) -> None: ...
    @property
    def description(self): ...
    @property
    def element_visuals(self) -> Iterator[ElementVisual]: ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementCreatedEvent, ElementShownEvent, ConnectionCreatedEvent, ConnectionShownEvent]]: ...
