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


class DuplicateSnippetCommand:
    def __init__(
        self,
        diagram: Diagram,
        snippet: Snippet
    ) -> None: ...
    def _do(self, ruler: QTRuler) -> None: ...
    @property
    def element_visuals(self) -> Iterator[ElementVisual]: ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementCreatedEvent, ElementShownEvent, ConnectionCreatedEvent, ConnectionShownEvent]]: ...
