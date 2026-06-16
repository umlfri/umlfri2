from ..base import Command as Command
from ..diagram import HideElementsCommand as HideElementsCommand
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NamedTuple
from umlfri2.application.events.model import ConnectionDeletedEvent as ConnectionDeletedEvent, DiagramDeletedEvent as DiagramDeletedEvent, ElementDeletedEvent as ElementDeletedEvent
from typing import (
    Iterator,
    Tuple,
    Union,
)
from umlfri2.application.events.diagram.connectionhidden import ConnectionHiddenEvent
from umlfri2.application.events.diagram.elementhidden import ElementHiddenEvent
from umlfri2.application.events.model.connectiondeleted import ConnectionDeletedEvent
from umlfri2.application.events.model.elementdeleted import ElementDeletedEvent
from umlfri2.model.element.elementobject import ElementObject
from umlfri2.qtgui.rendering.qtruler import QTRuler


class DeletedElementDescription(NamedTuple):
    index: Incomplete
    element: Incomplete

class DeletedDiagramDescription(NamedTuple):
    index: Incomplete
    diagram: Incomplete

class DeleteElementsCommand(Command):
    def __init__(self, elements: Tuple[ElementObject]) -> None: ...
    @property
    def description(self): ...
    def get_updates(
        self
    ) -> Iterator[Union[ElementDeletedEvent, ConnectionDeletedEvent, ElementHiddenEvent, ConnectionHiddenEvent]]: ...
